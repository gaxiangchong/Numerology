
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models import (
    User, UserHistory, CreditLedgerEntry, Voucher,
    ReferralCreditGrant, PendingOrder, PasswordResetToken, _generate_referral_code
)
from extensions import db, migrate  # ✅ NEW
from flask_bcrypt import Bcrypt
from translations import get_translation, get_current_language, set_language

from datetime import datetime, timedelta
import stripe, json, smtplib, os, secrets
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load .env for GOOGLE_GEMINI_API_KEY etc. Try python-dotenv, then simple file read
def _load_dotenv(path):
    """Simple .env loader: KEY=value per line, skip comments and empty lines."""
    if not os.path.isfile(path):
        return
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' in line:
                    k, _, v = line.partition('=')
                    k, v = k.strip(), v.strip()
                    if k and k not in os.environ:
                        if len(v) >= 2 and (v[0], v[-1]) in (('"', '"'), ("'", "'")):
                            v = v[1:-1]
                        os.environ[k] = v
    except Exception:
        pass

_app_dir = os.path.dirname(os.path.abspath(__file__))
_env_root = os.path.join(os.path.dirname(_app_dir), '.env')
_env_mysite = os.path.join(_app_dir, '.env')
try:
    from dotenv import load_dotenv
    load_dotenv(_env_root)
    load_dotenv(_env_mysite)
except ImportError:
    _load_dotenv(_env_root)
    _load_dotenv(_env_mysite)

# Replace with your real test keys
stripe.api_key = "sk_test_51SA4PtPiKknSy39RC5uqzBKr1PSAEG2iCzlhtOKI0b6zK8qpECGCw1nZpq3tHZwbIDrDIK8hhZ8xofYucSmIJsg100FI2lDUDD"

YOUR_DOMAIN = "http://127.0.0.1:5000"

app = Flask(__name__)


""" from flask_migrate import Migrate
migrate = Migrate(app, db) """

app.secret_key = 'your_secret_key'  # Needed for sessions

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI') or 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Mail (forgot password). Set env vars or leave unset to disable.
# See FORGOT_PASSWORD_SETUP.md for free options (Gmail, Resend, Brevo).
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', '')       # e.g. smtp.gmail.com
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', '587'))
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'true').lower() in ('1', 'true', 'yes')
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME', '')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD', '')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', app.config['MAIL_USERNAME'])
app.config['PASSWORD_RESET_EXPIRY_HOURS'] = int(os.environ.get('PASSWORD_RESET_EXPIRY_HOURS', '1'))

db.init_app(app)
bcrypt = Bcrypt(app)

migrate.init_app(app, db)

# Mock database (you can switch to SQLite later)
""" users = {
    "test@example.com": {
        "password": generate_password_hash("123456"),
        "is_pro": True,
        "pro_until": None,  # Optional
        "referrals": 0
    }
} """

with app.app_context():
    db.create_all()

# --- Helpers: credit balance, admin check ---
def get_credit_balance_cents(user_id):
    if not user_id:
        return 0
    from sqlalchemy import func
    credits = db.session.query(func.coalesce(func.sum(CreditLedgerEntry.amount_cents), 0)).filter(
        CreditLedgerEntry.user_id == user_id,
        CreditLedgerEntry.type == 'CREDIT'
    ).scalar() or 0
    debits = db.session.query(func.coalesce(func.sum(CreditLedgerEntry.amount_cents), 0)).filter(
        CreditLedgerEntry.user_id == user_id,
        CreditLedgerEntry.type.in_(['DEBIT', 'REVERSAL'])
    ).scalar() or 0
    return max(0, int(credits) - int(debits))

def require_admin(f):
    from functools import wraps
    @wraps(f)
    def inner(*args, **kwargs):
        if not session.get('user'):
            flash('请先登录', 'error')
            return redirect(url_for('login'))
        user = User.query.filter_by(email=session['user']).first()
        if not user or not getattr(user, 'is_admin', False):
            flash('需要管理员权限', 'error')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return inner

# Referral bonus amount (store credit in cents). e.g. 500 = RM5
REFERRAL_BONUS_CENTS = 500
# To make a user admin: UPDATE user SET is_admin=1 WHERE email='your@email.com';
# Plan base prices in cents (for credit/voucher calculation)
PLAN_PRICE_CENTS = {'monthly': 1390, 'annual': 11900}

# Add translation context processor
@app.context_processor
def inject_translations():
    out = {
        't': lambda key: get_translation(key, get_current_language()),
        'current_language': get_current_language()
    }
    if session.get('user'):
        u = User.query.filter_by(email=session['user']).first()
        if u:
            out['credit_balance_cents'] = get_credit_balance_cents(u.id)
            out['referral_code'] = getattr(u, 'referral_code', None)
            out['is_admin'] = getattr(u, 'is_admin', False)
        else:
            out['credit_balance_cents'] = 0
            out['referral_code'] = None
            out['is_admin'] = False
    else:
        out['credit_balance_cents'] = 0
        out['referral_code'] = None
        out['is_admin'] = False
    return out


# Define the pair mappings
pair_mappings = {
    '13': '天医[1]',
    '31': '天医[1]',
    '68': '天医[2]',
    '86': '天医[2]',
    '49': '天医[3]',
    '94': '天医[3]',
    '27': '天医[4]',
    '72': '天医[4]',

    '19': '延年[1]',
    '91': '延年[1]',
    '78': '延年[2]',
    '87': '延年[2]',
    '43': '延年[3]',
    '34': '延年[3]',
    '26': '延年[4]',
    '62': '延年[4]',

    '14': '生气[1]',
    '41': '生气[1]',
    '76': '生气[2]',
    '67': '生气[2]',
    '93': '生气[3]',
    '39': '生气[3]',
    '28': '生气[4]',
    '82': '生气[4]',

    '11': '伏位[1]',
    '22': '伏位[1]',
    '88': '伏位[2]',
    '99': '伏位[2]',
    '66': '伏位[3]',
    '77': '伏位[3]',
    '33': '伏位[4]',
    '44': '伏位[4]',

    '12': '绝命[1]',
    '21': '绝命[1]',
    '69': '绝命[2]',
    '96': '绝命[2]',
    '48': '绝命[3]',
    '84': '绝命[3]',
    '37': '绝命[4]',
    '73': '绝命[4]',

    '17': '祸害[1]',
    '71': '祸害[1]',
    '89': '祸害[2]',
    '98': '祸害[2]',
    '46': '祸害[3]',
    '64': '祸害[3]',
    '32': '祸害[4]',
    '23': '祸害[4]',

    '18': '五鬼[1]',
    '81': '五鬼[1]',
    '79': '五鬼[2]',
    '97': '五鬼[2]',
    '36': '五鬼[3]',
    '63': '五鬼[3]',
    '42': '五鬼[4]',
    '24': '五鬼[4]',

    '16': '六煞[1]',
    '61': '六煞[1]',
    '74': '六煞[2]',
    '47': '六煞[2]',
    '38': '六煞[3]',
    '83': '六煞[3]',
    '92': '六煞[4]',
    '29': '六煞[4]'
}

ending_financial_warnings = {
    "绝命": "冲动消费，投资血亏容易让人花钱如流水",
    "五鬼": "意外破财，财务丢失，钱不经意“蒸发”",
    "六煞": "情绪消费，人情破财，心情不好狂消费，钱用在安抚情绪",
    "祸害": "口舌破财，健康耗财，容易吵架赔钱，赚多留不住",
    "伏位": "保守漏财，错失良机，钱在银行悄悄贬值"
}


# Define the secondary group mappings
group_mappings = {
    '413': '有贵人给钱',
    '714': '有痪或有小人你不在意看得开 | 开口就有贵人来 | 生病不在乎，严重就危险',
    '416': '贵人让你抱怨可以买房',
    '417': '男朋友抱怨 | 贵人 = 小人《好心办坏事)',
    '914': '压力大不在平',
    '418': '贵人给建议',
    '4187': '贵人给建议会考虑',
    '314': '有钱就开心 ，就有贵人来，用心谈',
    '148': '朋友花钱',
    '767': '不积极，混日子',
    '917': '工作上犯小人工作做得抱怨',
    '3119': '钱稳定',
    '2019': '同性恋',
    '192': '能量低来自19的压力',
    '913': '付出有回报',
    '194': '付出多收获少',
    '816': '作的不开心不一定是工作的压力 | 癌症',
    '912': '过度自信破财',
    '317': '婚后抱怨，吵架',
    '1372': '工资越来越少收入不稳定',
    '312': '逢赌必输，有钱就会去赌',
    '133': '钱越来越少',
    '311': '钱持续有',
    '1312': '拼命工作赚钱但存不住钱',
    '316': '钱用到家里',
    '678': '主管格局',
    '318': '钱瞬间就没了',
    '319': '老板 / 主管格局对感情负责',
    '811': '长时间想调整，2次血光，心脏病反复',
    '711': '病不会好',
    '103': '感情不好只适合宗教，命理师使用',
    '108': '感情不好只适合宗教，命理师使用',
    '177': '持续抱怨',
    '911': '想得多，工作被动 | 制五鬼',
    '102': '为绝命组合,这样的人千万小心',
    '609': '为绝命组合,这样的人千万小心',
    '804': '为绝命组合,这样的人千万小心',
    '307': '为绝命组合,这样的人千万小心',
    '218': '破财后注意血光',
    '216': '钱用到家里买房',
    '121': '容易产生官司，离婚也敢分手',
    '217': '投资破财，破财会有抱怨，破财后生病 | 人比较胖，挑食，挑喜欢的吃，不在乎营养',
    '48': '表示官司',
    '484': '小心官司缠身',
    '213': '做大事，越做越有钱',
    '219': '有理财观念，但是没钱',
    '1214': '拼命工作，做得很开心',
    '2018': '想法偏激',
    '814': '喜欢动脑筋',
    '368': '收红包',
    '3068': '私下收红包',
    '798': '业务容易撞车',
    '36867': '红包吃得很开心',
    '813': '81的工作赚到13的钱',
    '819': '聪明绝项、策划',
    '907': '想换工作，因为0换不了',
    '812': '只要有想法，就会破财 | 做金融 / 培训 / 互联网赚钱，【动脑来的钱存不住】',
    '612': '女人会让你破财家、店、公司会破财',
    '2016': '一夜情，脚踏两只船',
    '614': '花花公子花心',
    '6l7': '阳宅出问题，情绪来了说话很难听，房屋风水有问题',
    '618': '癌症',
    '3617': '阴宅出问题',
    '83': '表示抑郁',
    '383': '做事情犹豫不决',
    '613': '买房子带来13的大钱',
    '9217': '女人抱怨家里开销大',
    '619': '顾家买大房',
    '16': '容易有情绪',
    '106': '压抑情绪',
    '166': '持续有情绪',
    '712': '小人会让你破财、【人比较胖，挑食，挑喜欢的吃，不在乎营养】',
    '7168': '开店赚钱',
    '719': '挑好的吃说话大声',
    '713': '多说话来钱',
    '806':'财富隐藏了，钱财虽多，但容易被套牢',
    '608': '财富隐藏了，钱财虽多，但容易被套牢',
    '856':'财富有，但赚钱辛苦',
    '658':'财富有，但赚钱辛苦',
    '860':'财富没有了',
    '680':'财富没有了',
    '865':'财富越来越多',
    '685':'财富越来越多'

}

# Define special conditions and their corresponding definitions
special_conditions = {
    '生气+延年': '主管非老板，延年大小决定格局大小',
    '生气+绝命': '朋友破财，不能合作，单干',
    '延年+六煞': '工作做得抑郁不开心',
    '延年+生气': '工作做得开心，小能量到大能量越来越开心',
    '绝命+五鬼': '绝命喜欢赌，赚到的钱转眼就没了',
    '绝命+天医': '逢赌必赢、少说话来钱',
    '绝命+生气': '花钱不手软，舍得花钱开心',
    '绝命+延年': '可以买房',
    '五鬼+延年+天医': '宗教命理，动头脑，工作类型',
    '五鬼+六煞': '抱怨，不得志，有天分用不出来',
    '六煞+生气': '偏桃花喜欢谈恋爱',
    '祸害+六煞': '动气、做店面生意、以口为业',
    '祸害+天医': '开口来钱、开口有桃花、口吐莲花',
}

energy_descriptions = {
    "天医": {
        "title": "天医磁场",
        "优点": "聪明善良，乐于助人，单纯开阔，象征财富、婚缘、福报，学习能力强，财运事业佳。",
        "缺点": "企图心小，没主见，单纯易被骗，感情路多波折。",
        "事业": "医生、心理学、宗教、心理疗愈，财路宽广，第六感强，投资回报好。",
        "健康": "血液循环、心脑血管、五官疾病。"
    },
    "生气": {
        "title": "生气磁场",
        "优点": "乐观开朗，生命力旺盛，花钱大方，贵人多，人缘好，活泼友善，容易交朋友。",
        "缺点": "安于现状，上进心弱，随遇而安，懒散，容易被骗，破财。",
        "事业": "服务业，有意外之财，适合投资，容易逢凶化吉。",
        "健康": "肠胃病、心脏病、精神病、五官疾病。"
    },
    "延年": {
        "title": "延年磁场",
        "优点": "有领导力，有责任心，心地善良，敢于承担，正义感强，保护弱者，寿命较长。",
        "缺点": "固执不变通，大男子主义或女性强势，压力大，不易接受意见。",
        "事业": "主导性强，专业能力佳，劳碌但能当领导。",
        "健康": "心脏病、精神病、颈椎病、肩周炎、掉发。"
    },
    "伏位": {
        "title": "伏位磁场",
        "优点": "潜力大，耐性毅力强，把握机会，不鸣则已，一鸣惊人，逻辑强，顾家型。",
        "缺点": "保守固执，缺乏变通，缺乏自信与冒险精神，孤独纠结。",
        "事业": "研究、分析类行业，偏稳定保守。",
        "健康": "脑部、失眠、头晕、心脏及隐藏性疾病。"
    },
    "祸害": {
        "title": "祸害磁场",
        "优点": "口才好，能说会道，八面玲珑，口福好，靠口才带财。",
        "缺点": "爱争辩，脾气暴躁，好胜心强，爱指责人，斤斤计较，抱怨多。",
        "事业": "讲师、教育、销售、律师、业务、娱乐表演；易被骗破财。",
        "健康": "车祸、意外、体质差、抵抗力差、呼吸疾病。"
    },
    "六煞": {
        "title": "六煞磁场",
        "优点": "聪明变通，社交强，情感丰富，爱美有魅力，异性缘佳，初见好印象。",
        "缺点": "敏感多疑，优柔寡断，情绪波动，消极抑郁，耳根软，爱传闲话。",
        "事业": "美容、美发、医美、女性行业，靠人脉得财，守财不易。",
        "健康": "肠胃病、皮肤病、抑郁症、失眠，严重者癌症。"
    },
    "绝命": {
        "title": "绝命磁场",
        "优点": "头脑灵活，记忆好，会赚钱，目标清晰，胆大敢拼，善良正义，金融投资有收获。",
        "缺点": "冲动暴躁，固执自负，好胜心强，赌性重，易有官司。",
        "事业": "冒险行业，如股票、房地产、金融、赌博，赚钱快但风险大。",
        "健康": "免疫力低、大病、肝肾疾病、糖尿病、劳损。"
    },
    "五鬼": {
        "title": "五鬼磁场",
        "优点": "才华横溢，聪明多变，学习力强，心机谋略佳，善于出奇制胜。",
        "缺点": "城府深，特立独行，反复无常，不走正道，不信任他人，爱熬夜。",
        "事业": "宗教、策划、贸易、偏门生意，工作不稳定。",
        "健康": "妇科、肺病、心脏病、脑部病、免疫力差、中风。"
    }
}




def convert_alpha_to_numbers(input_data):
    # Convert alphabetic characters to their corresponding numbers
    converted_input = []
    for char in str(input_data):
        if char == ' ':
            continue  # Skip spaces
        if char.isalpha():
            # Convert lowercase or uppercase letters to numbers (a=1, b=2, ..., z=26)
            converted_input.append(str(ord(char.lower()) - ord('a') + 1))
        else:
            converted_input.append(char)  # Keep non-alphabetic characters as is
    return ''.join(converted_input)

from collections import Counter, defaultdict

from collections import defaultdict, Counter

def analyze_number_pairs(input_data):
    group_to_pairs = defaultdict(list)
    detailed_group_rows = []

    number_str = convert_alpha_to_numbers(input_data)

    filtered_number = []
    removed_zeros = set()
    removed_fives = set()

    for i, char in enumerate(number_str):
        if char not in {'0', '5'}:
            filtered_number.append(char)
        elif char == '0':
            removed_zeros.add(i)
        elif char == '5':
            removed_fives.add(i)

    filtered_number = ''.join(filtered_number)

    pairs = []
    mapped_only = []

    for i in range(len(filtered_number) - 1):
        pair = filtered_number[i:i + 2]

        original_indices = [i, i + 1]
        original_indices_in_full_number = []
        current_filtered_index = 0
        for j in range(len(number_str)):
            if number_str[j] not in {'0', '5'}:
                if current_filtered_index in original_indices:
                    original_indices_in_full_number.append(j)
                current_filtered_index += 1

        # Count zeros and fives that affect this pair
        zero_count = 0
        five_count = 0
        
        # Count 5s between the pair digits (amplify the pair)
        if len(original_indices_in_full_number) >= 2:
            for idx in range(original_indices_in_full_number[0] + 1, original_indices_in_full_number[1]):
                if idx in removed_zeros:
                    zero_count += 1
                if idx in removed_fives:
                    five_count += 1

        if pair in pair_mappings:
            base_type = pair_mappings[pair].split('[')[0]
            definition = pair_mappings[pair]

            # ✅ Enhanced 伏位 logic
            if base_type == '伏位':
                prev_type = None
                next_type = None

                if i > 0:
                    prev_pair = filtered_number[i - 1:i + 1]
                    if prev_pair in pair_mappings:
                        ptype = pair_mappings[prev_pair].split('[')[0]
                        if ptype != '伏位':
                            prev_type = ptype

                if i + 2 <= len(filtered_number):
                    next_pair = filtered_number[i + 1:i + 3]
                    if next_pair in pair_mappings:
                        ntype = pair_mappings[next_pair].split('[')[0]
                        if ntype != '伏位':
                            next_type = ntype

                if prev_type or next_type:
                    left = prev_type if prev_type else ''
                    right = next_type if next_type else ''
                    definition = f"伏位（{left}→{right}）"

            # Add amplification markers based on 5s
            if zero_count > 0:
                definition += '(隐)'
            if five_count > 0:
                # Add "显" for each 5 (amplification)
                definition += '显' * five_count

            pairs.append(definition)
            mapped_only.append(pair_mappings[pair])

            # Stats for group rows
            group_to_pairs[base_type].append(pair)
            try:
                level = pair_mappings[pair].split('[')[-1].replace(']', '')
                level_int = int(level)
                base_energy_score = max(0, 100 - (level_int - 1) * 25)
                
                # Apply amplification based on 5s (20% per 5)
                amplification_multiplier = 1 + (five_count * 0.2)
                energy_score = int(base_energy_score * amplification_multiplier)
            except:
                energy_score = 0

            detailed_group_rows.append({
                'group': base_type,
                'pair': pair,
                'energy': f"{energy_score}%",
                'amplification': five_count,
                'base_energy': base_energy_score if 'base_energy_score' in locals() else 0
            })
        else:
            pairs.append(pair)

    # Frequency stats - now accounting for amplification
    frequency = dict(Counter(mapped_only))
    total_mapped = sum(frequency.values())

    percentage = {}
    group_summary = defaultdict(int)
    energy_score_by_group = defaultdict(list)

    # Create a mapping of pairs to their amplification data
    pair_amplification = {}
    for row in detailed_group_rows:
        pair_amplification[row['pair']] = {
            'amplification': row['amplification'],
            'base_energy': row['base_energy']
        }

    for key, count in frequency.items():
        base_type = key.split('[')[0]
        level = key.split('[')[-1].replace(']', '')

        try:
            level_int = int(level)
            base_energy_score = max(0, 100 - (level_int - 1) * 25)
            
            # Calculate average amplification for this pair type
            total_amplification = 0
            amplification_count = 0
            for pair, data in pair_amplification.items():
                if pair_mappings.get(pair) == key:
                    total_amplification += data['amplification']
                    amplification_count += 1
            
            avg_amplification = total_amplification / amplification_count if amplification_count > 0 else 0
            amplification_multiplier = 1 + (avg_amplification * 0.2)
            energy_score = int(base_energy_score * amplification_multiplier)
        except:
            energy_score = 0

        percentage[key] = {
            'count': count,
            'percent': round((count / total_mapped) * 100, 1) if total_mapped > 0 else 0,
            'energy': f"{energy_score * count}%",
            'amplification': avg_amplification if 'avg_amplification' in locals() else 0
        }

        group_summary[base_type] += count
        energy_score_by_group[base_type].extend([energy_score] * count)

    grouped_percentage = {}
    for group, count in group_summary.items():
        grouped_percentage[group] = {
            'count': count,
            'percent': round((count / total_mapped) * 100, 1) if total_mapped > 0 else 0
        }

    grouped_energy_percent = {}
    for group, values in energy_score_by_group.items():
        grouped_energy_percent[group] = sum(values)

    # Keep original grouped_stats without amplification markers in group names
    enhanced_grouped_stats = grouped_percentage.copy()

    # Ending warning logic
    last_pair = mapped_only[-1] if mapped_only else None
    ending_warning = None

    if last_pair:
        group_name = last_pair.split('[')[0]
        ending_warning = ending_financial_warnings.get(group_name)

    return pairs, percentage, enhanced_grouped_stats, grouped_energy_percent, ending_warning, group_to_pairs, detailed_group_rows



def perform_secondary_check(input_data):
    # Convert alphabetic characters to numbers
    number_str = convert_alpha_to_numbers(input_data)

    # Check if any group number exists in the input
    secondary_results = []
    for group, definition in group_mappings.items():
        if group in number_str:
            secondary_results.append(definition)

    return secondary_results

def check_special_conditions(primary_result):
    """
    Check if any special conditions are met in the primary analysis results.
    Args:
        primary_result (list): List of results from the primary analysis.
    Returns:
        list: List of special definitions that match the conditions.
    """
    special_definitions = []

    # Parse the primary result to keep only the first two letters
    parsed_result = parse_primary_result(primary_result)

    # Convert the list of results into a string for easier checking
    result_str = " ".join(parsed_result)

    # Check each special condition
    for condition, definition in special_conditions.items():
        # Replace '+' with a space to match the format of the result string
        if condition.replace("+", " ") in result_str:
            special_definitions.append(definition)

    return special_definitions


# Function to parse and keep only the first two letters of each item
def parse_primary_result(primary_result):
    """
    Keep only the first two letters of each item in the primary_result list.
    Args:
        primary_result (list): List of results from the primary analysis.
    Returns:
        list: List of parsed results with only the first two letters.
    """
    parsed_result = [item[:2] for item in primary_result]
    return parsed_result


@app.route('/')
def landing():
    """Landing page: intro, testimonials, CTAs. Logo links here."""
    return render_template('landing.html')


@app.route('/app', methods=['GET', 'POST'])
def index():
    """Main analysis app. Nav 'Home' links here."""
    if 'user' not in session:
        flash("请先登录以使用分析功能", "error")
        return redirect(url_for('login'))


    input_data = None
    primary_result = None
    pair_stats = {}
    grouped_stats = {}
    grouped_energy = {}
    ending_warning = None
    secondary_result = None
    special_definitions = None
    sorted_profiles = []



    if request.method == 'POST':
        input_data = request.form['input_data']

        # Analyze number
        primary_result, pair_stats, grouped_stats, grouped_energy, ending_warning, group_to_pairs, detailed_group_rows = analyze_number_pairs(input_data)
        
        # Save to history if user is logged in
        if session.get('user'):
            user = User.query.filter_by(email=session['user']).first()
            if user:
                # Check if this input already exists for this user
                existing_history = UserHistory.query.filter_by(
                    user_id=user.id, 
                    input_data=input_data
                ).first()
                
                if not existing_history:
                    # Create new history entry
                    new_history = UserHistory(
                        user_id=user.id,
                        input_data=input_data
                    )
                    db.session.add(new_history)
                    
                    # Keep only the last 10 entries per user
                    user_histories = UserHistory.query.filter_by(user_id=user.id).order_by(UserHistory.created_at.desc()).all()
                    if len(user_histories) > 10:
                        for old_history in user_histories[10:]:
                            db.session.delete(old_history)
                    
                    db.session.commit()

        # If logged in and PRO, show advanced features
        if session.get('user') and session.get('is_pro'):
            secondary_result = perform_secondary_check(input_data)
            special_definitions = check_special_conditions(primary_result)

            # Prepare sorted energy profiles
            profile_list = []
            for group, data in grouped_stats.items():
                if group in energy_descriptions:
                    profile_list.append((group, energy_descriptions[group], data['percent']))
            profile_list.sort(key=lambda x: x[2], reverse=True)
            sorted_profiles = profile_list

            detailed_group_rows=detailed_group_rows if input_data else [],

    # Get recent numbers for logged-in users
    recent_numbers = []
    if session.get('user'):
        user = User.query.filter_by(email=session['user']).first()
        if user:
            recent_histories = UserHistory.query.filter_by(user_id=user.id).order_by(UserHistory.created_at.desc()).limit(10).all()
            recent_numbers = [history.input_data for history in recent_histories]

    return render_template('index.html',
                           input_data=input_data,
                           primary_result=primary_result,
                           pair_stats=pair_stats,
                           grouped_stats=grouped_stats,
                           grouped_energy=grouped_energy,
                           ending_warning=ending_warning,
                           secondary_result=secondary_result,
                           special_definitions=special_definitions,
                           sorted_profiles=sorted_profiles,
                           group_to_pairs=group_to_pairs if input_data else {},
                           detailed_group_rows=detailed_group_rows if input_data else [],
                           grouped_stats_json=grouped_stats,
                           recent_numbers=recent_numbers,
                           is_pro=session.get('is_pro', False),
                           user=session.get('user'))


@app.route('/ai')
def ai_page():
    """AI chat page (Pro only). Chat-style UI, no history."""
    if not session.get('user'):
        return redirect(url_for('login'))
    if not session.get('is_pro'):
        flash(get_translation('ai_page_pro_required', get_current_language()), 'error')
        return redirect(url_for('pricing'))
    try:
        from gemini_service import is_available as gemini_is_available
        gemini_available = gemini_is_available()
    except Exception:
        gemini_available = False
    return render_template('ai.html', gemini_available=gemini_available)


@app.route('/ask_ai', methods=['POST'])
def ask_ai():
    """Pro-only: ask Gemini (with optional file search) about a number/car plate."""
    if not session.get('user'):
        return jsonify({'error': 'Login required'}), 401
    if not session.get('is_pro'):
        return jsonify({'error': 'Pro subscription required'}), 403
    data = request.get_json(silent=True) or {}
    question = (data.get('question') or request.form.get('question') or '').strip()
    if not question:
        return jsonify({'error': 'Question is required'}), 400
    number_context = (data.get('number_context') or data.get('input_data') or request.form.get('number_context') or '').strip() or None
    try:
        from gemini_service import ask as gemini_ask
        answer = gemini_ask(question, number_context=number_context)
        return jsonify({'answer': answer})
    except (ImportError, ModuleNotFoundError) as e:
        err = str(e).strip() or 'google.genai not found'
        return jsonify({
            'error': (
                'GenAI SDK not available in this Python environment. '
                'Install with: pip install google-genai — then restart Flask using the *same* Python/venv (e.g. activate venv, run python app.py). '
                'Detail: %s' % err
            )
        }), 503
    except ValueError as e:
        return jsonify({'error': str(e)}), 503
    except Exception as e:
        return jsonify({'error': str(e)}), 500




@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        ref = request.args.get('ref')
        if ref:
            session['referral_ref'] = ref.strip()[:20]
        return render_template('register.html', ref=ref)

    email = password = None  # ✅ always declared

    if request.is_json:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
    else:
        email = request.form.get('email')
        password = request.form.get('password')

    if not email or not password:
        if request.is_json:
            return jsonify({'message': 'Email and password are required'}), 400
        else:
            flash("请输入邮箱和密码", "error")
            return redirect(url_for('register'))

    if User.query.filter_by(email=email).first():
        if request.is_json:
            return jsonify({'message': 'User already exists'}), 400
        else:
            flash("用户已存在", "error")
            return redirect(url_for('register'))

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Referral: ref can be in query (?ref=CODE) or session (set when landing with ref)
    ref_code = request.args.get('ref') or request.form.get('ref') or session.pop('referral_ref', None)
    referred_by_id = None
    if ref_code:
        referrer = User.query.filter_by(referral_code=ref_code.upper()).first()
        if referrer and referrer.email != email:
            referred_by_id = referrer.id

    new_user = User(email=email, password=hashed_password, referred_by_id=referred_by_id)
    # Unique referral code for this user (for sharing)
    for _ in range(5):
        code = _generate_referral_code()
        if not User.query.filter_by(referral_code=code).first():
            new_user.referral_code = code
            break
    if not new_user.referral_code:
        new_user.referral_code = _generate_referral_code() + str(new_user.id)[:2]
    db.session.add(new_user)
    db.session.commit()

    if request.is_json:
        return jsonify({'message': 'User registered successfully', 'is_pro': new_user.is_pro}), 201
    else:
        flash("注册成功，请登录", "success")
        return redirect(url_for('login'))



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            session['user'] = email
            session['is_pro'] = user.is_pro
            session['is_admin'] = getattr(user, 'is_admin', False)
            return redirect(url_for('index'))
        else:
            flash("登录失败，请检查邮箱或密码", "error")
    return render_template('login.html')



def _send_password_reset_email(to_email, reset_url, lang='en'):
    """Send reset link via SMTP. No-op if MAIL_SERVER not configured."""
    if not app.config.get('MAIL_SERVER') or not app.config.get('MAIL_USERNAME') or not app.config.get('MAIL_PASSWORD'):
        return False
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = 'Reset your password - Numerology' if lang == 'en' else '重置密码 - 命理分析'
        msg['From'] = app.config.get('MAIL_DEFAULT_SENDER') or app.config['MAIL_USERNAME']
        msg['To'] = to_email
        text = f"Reset your password: {reset_url}\nLink valid for 1 hour."
        if lang == 'zh':
            text = f"请点击以下链接重置密码：{reset_url}\n链接1小时内有效。"
        msg.attach(MIMEText(text, 'plain', 'utf-8'))
        with smtplib.SMTP(app.config['MAIL_SERVER'], app.config['MAIL_PORT']) as s:
            if app.config.get('MAIL_USE_TLS'):
                s.starttls()
            s.login(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
            s.sendmail(msg['From'], to_email, msg.as_string())
        return True
    except Exception as e:
        if app.debug:
            print('Mail send failed:', e)
        return False


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = (request.form.get('email') or '').strip().lower()
        lang = get_current_language()
        if not email:
            flash('请输入邮箱', 'error') if lang == 'zh' else flash('Please enter your email', 'error')
            return redirect(url_for('forgot_password'))
        user = User.query.filter_by(email=email).first()
        if not user:
            # Don't reveal whether email exists
            flash('若该邮箱已注册，您将收到重置链接。请查收邮件。', 'success') if lang == 'zh' else flash('If that email is registered, you will receive a reset link. Check your inbox.', 'success')
            return redirect(url_for('login'))
        # Invalidate any existing tokens for this user
        PasswordResetToken.query.filter_by(user_id=user.id).delete()
        token_str = secrets.token_urlsafe(32)
        expires = datetime.utcnow() + timedelta(hours=app.config['PASSWORD_RESET_EXPIRY_HOURS'])
        t = PasswordResetToken(user_id=user.id, token=token_str, expires_at=expires)
        db.session.add(t)
        db.session.commit()
        reset_url = request.url_root.rstrip('/') + url_for('reset_password', token=token_str)
        if _send_password_reset_email(user.email, reset_url, lang):
            flash('已发送重置链接到您的邮箱，请查收。', 'success') if lang == 'zh' else flash('A reset link has been sent to your email.', 'success')
        else:
            flash('邮件发送失败。请检查服务器邮件配置，或联系管理员。', 'error') if lang == 'zh' else flash('Failed to send email. Check server mail config or contact admin.', 'error')
        return redirect(url_for('login'))
    return render_template('forgot_password.html')


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    t = PasswordResetToken.query.filter_by(token=token).first()
    if not t or t.used_at or t.expires_at < datetime.utcnow():
        flash('链接无效或已过期，请重新申请重置密码。', 'error') if get_current_language() == 'zh' else flash('Link invalid or expired. Please request a new reset.', 'error')
        return redirect(url_for('forgot_password'))
    if request.method == 'POST':
        password = request.form.get('password') or ''
        if len(password) < 6:
            flash('密码至少6位', 'error') if get_current_language() == 'zh' else flash('Password must be at least 6 characters', 'error')
            return render_template('reset_password.html', token=token)
        user = t.user
        user.password = bcrypt.generate_password_hash(password).decode('utf-8')
        t.used_at = datetime.utcnow()
        db.session.commit()
        flash('密码已更新，请登录。', 'success') if get_current_language() == 'zh' else flash('Password updated. Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('reset_password.html', token=token)


@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('is_pro', None)
    session.pop('is_admin', None)
    flash("已登出，请先登录以使用分析功能", "error")
    return redirect(url_for('login'))


@app.route('/profile')
def profile():
    if not session.get('user'):
        return redirect(url_for('login'))
    return render_template('profile.html')


@app.route('/clear_history', methods=['POST'])
def clear_history():
    if session.get('user'):
        user = User.query.filter_by(email=session['user']).first()
        if user:
            UserHistory.query.filter_by(user_id=user.id).delete()
            db.session.commit()
            flash("历史记录已清除", "success")
    return redirect(url_for('index'))

# DISABLED FOR TESTING - Create pro account functionality
# @app.route('/create_pro_account', methods=['GET', 'POST'])
# def create_pro_account():
#     """Create a pro account for testing purposes"""
#     if request.method == 'POST':
#         email = request.form.get('email')
#         password = request.form.get('password')
#         
#         if not email or not password:
#             flash("请输入邮箱和密码", "error")
#             return render_template('create_pro.html')
#         
#         # Check if user already exists
#         existing_user = User.query.filter_by(email=email).first()
#         if existing_user:
#             flash("用户已存在", "error")
#             return render_template('create_pro.html')
#         
#         # Create new pro user
#         hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
#         new_user = User(
#             email=email, 
#             password=hashed_password, 
#             is_pro=True
#         )
#         db.session.add(new_user)
#         db.session.commit()
#         
#         flash(f"Pro账户 {email} 创建成功！", "success")
#         return redirect(url_for('login'))
#     
#     return render_template('create_pro.html')

@app.route('/upgrade_to_pro', methods=['POST'])
def upgrade_to_pro():
    """Upgrade an existing account to pro"""
    if session.get('user'):
        user = User.query.filter_by(email=session['user']).first()
        if user:
            user.is_pro = True
            db.session.commit()
            session['is_pro'] = True
            flash("账户已升级为Pro版本！", "success")
        else:
            flash("用户不存在", "error")
    else:
        flash("请先登录", "error")
    return redirect(url_for('index'))

@app.route('/referral')
def referral():
    if not session.get('user'):
        flash('请先登录', 'error')
        return redirect(url_for('login'))
    user = User.query.filter_by(email=session['user']).first()
    if not user:
        return redirect(url_for('login'))
    if not user.referral_code:
        for _ in range(5):
            code = _generate_referral_code()
            if not User.query.filter_by(referral_code=code).first():
                user.referral_code = code
                db.session.commit()
                break
    balance_cents = get_credit_balance_cents(user.id)
    share_url = request.url_root.rstrip('/') + url_for('register') + '?ref=' + (user.referral_code or '')
    referral_count = ReferralCreditGrant.query.filter_by(referrer_id=user.id).count()
    return render_template('referral.html',
        referral_code=user.referral_code,
        share_url=share_url,
        balance_cents=balance_cents,
        referral_count=referral_count,
        bonus_cents=REFERRAL_BONUS_CENTS)

@app.route('/pricing')
def pricing():
    return render_template('pricing.html')

@app.route('/admin')
@require_admin
def admin_dashboard():
    total_users = User.query.count()
    pro_users = User.query.filter_by(is_pro=True).count()
    total_referrals = ReferralCreditGrant.query.count()
    voucher_available = Voucher.query.filter_by(status='AVAILABLE').count()
    voucher_used = Voucher.query.filter_by(status='USED').count()
    return render_template('admin/dashboard.html',
        total_users=total_users, pro_users=pro_users,
        total_referrals=total_referrals, voucher_available=voucher_available, voucher_used=voucher_used)

@app.route('/admin/vouchers')
@require_admin
def admin_vouchers():
    vouchers = Voucher.query.order_by(Voucher.created_at.desc()).all()
    return render_template('admin/vouchers.html', vouchers=vouchers)

@app.route('/admin/vouchers/create', methods=['GET', 'POST'])
@require_admin
def admin_voucher_create():
    if request.method == 'POST':
        code = (request.form.get('code') or '').strip().upper()
        discount_percent = request.form.get('discount_percent', type=int)
        valid_from_s = request.form.get('valid_from')
        valid_until_s = request.form.get('valid_until')
        if not code:
            flash('请输入优惠码', 'error')
            return redirect(url_for('admin_voucher_create'))
        if Voucher.query.filter_by(code=code).first():
            flash('该优惠码已存在', 'error')
            return redirect(url_for('admin_voucher_create'))
        if not (1 <= discount_percent <= 100):
            flash('折扣比例须在 1-100 之间', 'error')
            return redirect(url_for('admin_voucher_create'))
        try:
            valid_from = datetime.strptime(valid_from_s or '2000-01-01', '%Y-%m-%d')
            valid_until = datetime.strptime(valid_until_s or '2099-12-31', '%Y-%m-%d')
        except ValueError:
            flash('日期格式错误', 'error')
            return redirect(url_for('admin_voucher_create'))
        if valid_until < valid_from:
            flash('结束日期须晚于开始日期', 'error')
            return redirect(url_for('admin_voucher_create'))
        user = User.query.filter_by(email=session['user']).first()
        v = Voucher(code=code, status='AVAILABLE', discount_percent=discount_percent,
                    valid_from=valid_from, valid_until=valid_until, created_by_id=user.id if user else None)
        db.session.add(v)
        db.session.commit()
        flash('优惠券已创建', 'success')
        return redirect(url_for('admin_vouchers'))
    return render_template('admin/voucher_create.html')

@app.route('/admin/credit/grant', methods=['GET', 'POST'])
@require_admin
def admin_grant_credit():
    if request.method == 'POST':
        email = (request.form.get('email') or '').strip()
        amount_cents = request.form.get('amount_cents', type=int) or 0
        if not email or amount_cents <= 0:
            flash('请输入有效邮箱和金额（分）', 'error')
            return redirect(url_for('admin_grant_credit'))
        user = User.query.filter_by(email=email).first()
        if not user:
            flash('用户不存在', 'error')
            return redirect(url_for('admin_grant_credit'))
        admin_user = User.query.filter_by(email=session['user']).first()
        db.session.add(CreditLedgerEntry(
            user_id=user.id, type='CREDIT', amount_cents=amount_cents,
            reference_type='admin_grant', reference_id=str(admin_user.id) if admin_user else None,
            note='Admin grant'
        ))
        db.session.commit()
        flash('已为用户 %s 充值 %s 分' % (email, amount_cents), 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('admin/grant_credit.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/set_language/<language>')
def set_language_route(language):
    """Set language and redirect back to the previous page"""
    if language in ['en', 'zh']:
        set_language(language)
    return redirect(request.referrer or url_for('index'))

def _validate_voucher(code):
    """Returns (voucher, error_message). Voucher is None if invalid."""
    if not code or not code.strip():
        return None, None
    v = Voucher.query.filter_by(code=code.strip().upper(), status='AVAILABLE').first()
    if not v:
        return None, 'Voucher not found or already used'
    now = datetime.utcnow()
    if v.valid_from and now < v.valid_from:
        return None, 'Voucher not yet valid'
    if v.valid_until and now > v.valid_until:
        v.status = 'EXPIRED'
        db.session.commit()
        return None, 'Voucher has expired'
    return v, None

def _fulfill_order(order):
    """Apply credit DEBIT, mark voucher USED, set user is_pro. Call with order locked/committed after."""
    user = order.user
    if order.credit_applied_cents > 0:
        db.session.add(CreditLedgerEntry(
            user_id=user.id, type='DEBIT', amount_cents=order.credit_applied_cents,
            reference_type='purchase', reference_id=str(order.id), note='Subscription'
        ))
    if order.voucher_id:
        v = Voucher.query.get(order.voucher_id)
        if v:
            v.status = 'USED'
            v.used_at = datetime.utcnow()
            v.used_by_id = user.id
    user.is_pro = True
    extend_days = 365 if order.plan == 'annual' else 30
    if not user.pro_until or user.pro_until < datetime.utcnow():
        user.pro_until = datetime.utcnow() + timedelta(days=extend_days)
    else:
        user.pro_until += timedelta(days=extend_days)
    order.status = 'paid'
    order.paid_at = datetime.utcnow()
    db.session.commit()

@app.route('/upgrade')
def upgrade_success():
    """Stripe success redirect: fulfill PendingOrder (credit/voucher), set is_pro."""
    session_id = request.args.get('session_id')
    if not session_id:
        if session.get('user'):
            flash('订阅成功！', 'success')
        return redirect(url_for('index'))
    try:
        checkout = stripe.checkout.Session.retrieve(session_id)
        customer_email = checkout.get('customer_email') or (checkout.get('customer') and stripe.Customer.retrieve(checkout['customer']).email)
        if not customer_email and checkout.get('customer_details', {}).get('email'):
            customer_email = checkout['customer_details']['email']
    except Exception:
        return redirect(url_for('index'))
    if not customer_email:
        return redirect(url_for('index'))
    user = User.query.filter_by(email=customer_email).first()
    if user:
        order = PendingOrder.query.filter_by(stripe_session_id=session_id, user_id=user.id, status='pending').first()
        if order:
            _fulfill_order(order)
        else:
            user.is_pro = True
            extend_days = 30
            if not user.pro_until or user.pro_until < datetime.utcnow():
                user.pro_until = datetime.utcnow() + timedelta(days=extend_days)
            else:
                user.pro_until += timedelta(days=extend_days)
            db.session.commit()
    if session.get('user') == customer_email:
        session['is_pro'] = True
    flash('订阅成功！感谢您的支持。', 'success')
    return redirect(url_for('index'))

@app.route('/upgrade/<int:user_id>', methods=['POST'])
def upgrade(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    session['is_pro'] = True
    flash("您已成功订阅大师版！", "success")

    user.is_pro = True
    db.session.commit()

    return jsonify({'message': f'User {user.email} upgraded to paid'}), 200


@app.route('/subscribe/<plan>', methods=['GET', 'POST'])
def subscribe(plan):
    if plan not in PLAN_PRICE_CENTS:
        flash('无效的订阅类型', 'error')
        return redirect(url_for('pricing'))
    base_cents = PLAN_PRICE_CENTS[plan]
    price_lookup = {
        'monthly': 'price_1SAAlZPiKknSy39RarQrt1u2',
        'annual': 'price_1SAAnuPiKknSy39R0c4IZRMp'
    }
    price_id = price_lookup.get(plan)
    if not price_id:
        return "无效的订阅类型", 400

    if not session.get('user'):
        flash('请先登录', 'error')
        return redirect(url_for('login'))

    user = User.query.filter_by(email=session['user']).first()
    if not user:
        return redirect(url_for('login'))

    voucher = None
    discount_cents = 0
    voucher_code = (request.form.get('voucher_code') or request.args.get('voucher_code') or '').strip()
    if voucher_code:
        voucher, err = _validate_voucher(voucher_code)
        if err:
            flash(err, 'error')
            return redirect(url_for('pricing'))
        if voucher:
            discount_cents = base_cents * voucher.discount_percent // 100
    after_discount = max(0, base_cents - discount_cents)

    use_credit = request.form.get('use_credit') == '1' or request.args.get('use_credit') == '1'
    credit_balance = get_credit_balance_cents(user.id)
    credit_to_apply = min(credit_balance, after_discount) if use_credit else 0
    final_cents = max(0, after_discount - credit_to_apply)

    order = PendingOrder(
        user_id=user.id, plan=plan, amount_cents=final_cents,
        credit_applied_cents=credit_to_apply, voucher_id=voucher.id if voucher else None
    )
    db.session.add(order)
    db.session.commit()

    if final_cents == 0:
        _fulfill_order(order)
        session['is_pro'] = True
        flash('已使用余额/优惠券完成升级！', 'success')
        return redirect(url_for('index'))

    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'myr',
                'unit_amount': final_cents,
                'product_data': {
                    'name': '大师版 ' + ('月付' if plan == 'monthly' else '年付'),
                    'description': 'Numerology Master Plan'
                },
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=YOUR_DOMAIN + '/upgrade?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=YOUR_DOMAIN + '/pricing',
        customer_email=session.get('user'),
        metadata={'pending_order_id': str(order.id)}
    )
    order.stripe_session_id = checkout_session.id
    db.session.commit()
    return redirect(checkout_session.url, code=303)



@app.route('/pay')
def pay():
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'myr',
                'unit_amount': 1390,  # RM13.90 = 990 sen
                'product_data': {
                    'name': '升级为大师版',
                    'description': '解锁大师分析功能'
                },
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=YOUR_DOMAIN + '/upgrade',
        cancel_url=YOUR_DOMAIN + '/pricing',
    )
    return redirect(checkout_session.url, code=303)

import stripe
from flask import request, jsonify

@app.route('/stripe/webhook', methods=['POST'])
def stripe_webhook():
    payload = request.data
    sig_header = request.headers.get('stripe-signature')
    endpoint_secret = 'whsec_jmhO3wbKFNp9aee1IBILuccGxccOltdL'  # 🔐 replace with your webhook secret from Stripe

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError as e:
        return jsonify({'error': 'Invalid payload'}), 400
    except stripe.error.SignatureVerificationError:
        return jsonify({'error': 'Invalid signature'}), 400

    # 🎯 Handle successful payment (subscription or renewal)
    if event['type'] == 'invoice.paid':
        invoice = event['data']['object']
        subscription_id = invoice.get('subscription')
        customer_email = invoice.get('customer_email')

        user = User.query.filter_by(email=customer_email).first()
        if user:
            user.is_pro = True
            if subscription_id:
                user.stripe_subscription_id = subscription_id
            extend_days = 30
            if not user.pro_until or user.pro_until < datetime.utcnow():
                user.pro_until = datetime.utcnow() + timedelta(days=extend_days)
            else:
                user.pro_until += timedelta(days=extend_days)

            # Referral: grant referrer store credit once per referred user (idempotent)
            if getattr(user, 'referred_by_id', None) and user.referred_by_id != user.id:
                existing = ReferralCreditGrant.query.filter_by(
                    referrer_id=user.referred_by_id, referred_user_id=user.id
                ).first()
                if not existing:
                    entry = CreditLedgerEntry(
                        user_id=user.referred_by_id,
                        type='CREDIT',
                        amount_cents=REFERRAL_BONUS_CENTS,
                        reference_type='referral',
                        reference_id=str(user.id),
                        note='Referral bonus'
                    )
                    db.session.add(entry)
                    db.session.add(ReferralCreditGrant(
                        referrer_id=user.referred_by_id,
                        referred_user_id=user.id,
                        amount_cents=REFERRAL_BONUS_CENTS
                    ))
            db.session.commit()

    return jsonify({'status': 'success'}), 200



if __name__ == '__main__':
    app.run(debug=True)