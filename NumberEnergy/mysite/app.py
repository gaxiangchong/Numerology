
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models import (
    User, UserHistory, CreditLedgerEntry, Voucher,
    ReferralCreditGrant, ReferralUsageCreditGrant, PendingOrder, PasswordResetToken,
    UsageCreditEntry, LuckyNumberHistory, _generate_referral_code
)
from extensions import db, migrate  # ✅ NEW
from flask_bcrypt import Bcrypt
from translations import get_translation, get_current_language, set_language

from datetime import datetime, timedelta
import stripe, json, smtplib, os, secrets, random, re
import requests as _requests
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

YOUR_DOMAIN = "http://127.0.0.1:8050"

app = Flask(__name__)


""" from flask_migrate import Migrate
migrate = Migrate(app, db) """

app.secret_key = os.environ.get('SECRET_KEY') or 'd8f9c7a1e3b42c9f5a6d8e1b3c4f7a9e2d6c8b1a4f9e3d7c6b2a1e8f4c9d3a7'  # Production: set SECRET_KEY in env

# Database configuration (DATABASE_URL or SQLALCHEMY_DATABASE_URI)
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('SQLALCHEMY_DATABASE_URI') or
    os.environ.get('DATABASE_URL') or
    'sqlite:///users.db'
)
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
# Twilio Verify (WhatsApp OTP). Set TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_VERIFY_SERVICE_SID.
app.config['TWILIO_ACCOUNT_SID'] = os.environ.get('TWILIO_ACCOUNT_SID', '')
app.config['TWILIO_AUTH_TOKEN'] = os.environ.get('TWILIO_AUTH_TOKEN', '')
app.config['TWILIO_VERIFY_SERVICE_SID'] = os.environ.get('TWILIO_VERIFY_SERVICE_SID', '')

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
    # Add new credit columns to user table if missing (e.g. existing SQLite DB)
    try:
        from sqlalchemy import text
        if db.engine.url.get_dialect().name == 'sqlite':
            with db.engine.connect() as conn:
                cur = conn.execute(text("PRAGMA table_info(user)"))
                cols = [row[1] for row in cur]
                for col, sql in [
                    ('plan', "ALTER TABLE user ADD COLUMN plan VARCHAR(20) DEFAULT 'free'"),
                    ('credits_balance', 'ALTER TABLE user ADD COLUMN credits_balance INTEGER DEFAULT 0'),
                    ('credits_per_month', 'ALTER TABLE user ADD COLUMN credits_per_month INTEGER DEFAULT 10'),
                    ('credit_reset_at', 'ALTER TABLE user ADD COLUMN credit_reset_at DATETIME'),
                    ('display_name', 'ALTER TABLE user ADD COLUMN display_name VARCHAR(100)'),
                    ('phone', 'ALTER TABLE user ADD COLUMN phone VARCHAR(30)'),
                    ('mail_subscriber', 'ALTER TABLE user ADD COLUMN mail_subscriber BOOLEAN DEFAULT 0'),
                ]:
                    if col not in cols:
                        conn.execute(text(sql))
                conn.commit()
    except Exception:
        pass

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


def get_usage_credit_balance(user):
    """Return user's usage credit balance. If credit_reset_at has passed, grant monthly credits and advance reset."""
    if not user:
        return 0
    now = datetime.utcnow()
    reset_at = getattr(user, 'credit_reset_at', None)
    if reset_at is None:
        # Backfill for existing users: grant initial credits and set first reset
        per_month = getattr(user, 'credits_per_month', None) or CREDITS_FREE_PER_MONTH
        mail_bonus = 4 if getattr(user, 'mail_subscriber', False) else 0
        user.credits_per_month = per_month
        user.credits_balance = (user.credits_balance or 0) + per_month + mail_bonus
        user.credit_reset_at = now + timedelta(days=30)
        user.plan = getattr(user, 'plan', None) or 'free'
        db.session.add(UsageCreditEntry(
            user_id=user.id, type='monthly_grant', amount=per_month,
            reference_type='initial_backfill', reference_id=None
        ))
        db.session.commit()
        return max(0, user.credits_balance or 0)
    if now >= reset_at:
        per_month = getattr(user, 'credits_per_month', CREDITS_FREE_PER_MONTH) or CREDITS_FREE_PER_MONTH
        mail_bonus = 4 if getattr(user, 'mail_subscriber', False) else 0
        total_grant = per_month + mail_bonus
        user.credits_balance = (user.credits_balance or 0) + total_grant
        user.credit_reset_at = now + timedelta(days=30)
        db.session.add(UsageCreditEntry(
            user_id=user.id, type='monthly_grant', amount=total_grant,
            reference_type='monthly_reset', reference_id=None
        ))
        db.session.commit()
    return max(0, user.credits_balance or 0)


def deduct_usage_credits(user_id, amount, reference_type, reference_id=None):
    """Deduct usage credits. Returns True if successful (balance was >= amount)."""
    user = User.query.get(user_id)
    if not user:
        return False
    balance = get_usage_credit_balance(user)
    if balance < amount:
        return False
    user.credits_balance = (user.credits_balance or 0) - amount
    db.session.add(UsageCreditEntry(
        user_id=user_id, type=reference_type, amount=-amount,
        reference_type=reference_type, reference_id=reference_id
    ))
    db.session.commit()
    return True


def require_admin(f):
    from functools import wraps
    @wraps(f)
    def inner(*args, **kwargs):
        if not session.get('user'):
            flash(get_translation('msg_please_login', get_current_language()), 'error')
            return redirect(url_for('login'))
        user = User.query.filter_by(email=session['user']).first()
        if not user or not getattr(user, 'is_admin', False):
            flash(get_translation('msg_admin_required', get_current_language()), 'error')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return inner

# Referral bonus amount (store credit in cents). e.g. 500 = RM5
REFERRAL_BONUS_CENTS = 500
# To make a user admin: UPDATE user SET is_admin=1 WHERE email='your@email.com';

# --- Credit-based plans (usage credits per month) ---
# Free: 10/mo. Starter: RM39, 150. Pro: RM59, 500. Master: RM99, unlimited (99999).
CREDITS_FREE_PER_MONTH = 10
CREDITS_BY_PLAN = {
    'free': 10,
    'starter': 150,
    'pro': 500,
    'master': 99999,  # unlimited
    'monthly': 50,    # legacy
    'annual': 100,    # legacy
}
COST_NUMBER_ANALYSIS = 2
COST_AI_REQUEST = 3
COST_LUCKY_GENERATION = 1
REFERRAL_CREDITS_WHEN_STARTER = 20
REFERRAL_CREDITS_WHEN_PRO = 50
REFERRAL_CREDITS_WHEN_MASTER = 100

# Plan base prices in cents. Starter RM39, Pro RM59, Master RM99 (monthly only).
PLAN_PRICE_CENTS = {'starter': 3900, 'pro': 5900, 'master': 9900}
STRIPE_PRICE_IDS = {
    'starter': os.environ.get('STRIPE_PRICE_STARTER') or '',
    'pro': os.environ.get('STRIPE_PRICE_PRO') or '',
    'master': os.environ.get('STRIPE_PRICE_MASTER') or '',
}

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
            out['credit_balance'] = get_usage_credit_balance(u)
            out['user_plan'] = getattr(u, 'plan', None) or 'free'
            out['referral_code'] = getattr(u, 'referral_code', None)
            out['is_admin'] = getattr(u, 'is_admin', False)
        else:
            out['credit_balance_cents'] = 0
            out['credit_balance'] = 0
            out['user_plan'] = 'free'
            out['referral_code'] = None
            out['is_admin'] = False
    else:
        out['credit_balance_cents'] = 0
        out['credit_balance'] = 0
        out['user_plan'] = 'free'
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
    "五鬼": "意外破财，财务丢失，钱不经意蒸发",
    "六煞": "情绪消费，人情破财，心情不好狂消费，钱用在安抚情绪",
    "祸害": "口舌破财，健康耗财，容易吵架赔钱，赚多留不住",
    "伏位": "保守漏财，错失良机，钱在银行悄悄贬值"
}

# Lucky 4-digit generator: 六煞 + 生气 pairs only (from app pair_mappings)
LIU_SHA_PAIRS = ['16', '61', '74', '47', '38', '83', '92', '29']
SHENG_QI_PAIRS = ['14', '41', '76', '67', '93', '39', '28', '82']
# 阴阳五行 我克者为财: day_master -> 财 element -> lucky digits (河图: 水1,6 火4,9 木3,8 金2,7 土5,0)
DAY_MASTER_TO_WEALTH_DIGITS = {
    '木': [],   # 财=土 5,0 - no 5,0 in pairs, fallback to general
    '火': ['2', '7'],  # 财=金
    '土': ['1', '6'],  # 财=水
    '金': ['3', '8'],  # 财=木
    '水': ['4', '9'],  # 财=火
}

def _pairs_containing_digits(pair_list, digits):
    """Return pairs that contain any of the given digits."""
    if not digits:
        return pair_list
    return [p for p in pair_list if p[0] in digits or p[1] in digits]

def generate_lucky_4digit(mode='general', day_master=None):
    """
    Generate a 4-digit lucky number from 六煞 + 生气.
    mode: 'general' (any 六煞+生气) or 'personal' (filter by day_master 财 digits).
    Returns (four_digit_str, liu_sha_pair, sheng_qi_pair).
    """
    liu_sha = list(LIU_SHA_PAIRS)
    sheng_qi = list(SHENG_QI_PAIRS)
    if mode == 'personal' and day_master and day_master in DAY_MASTER_TO_WEALTH_DIGITS:
        digits = DAY_MASTER_TO_WEALTH_DIGITS[day_master]
        if digits:
            liu_sha = _pairs_containing_digits(liu_sha, digits)
            sheng_qi = _pairs_containing_digits(sheng_qi, digits)
        # if digits empty (木) or no match, keep full lists
    if not liu_sha:
        liu_sha = list(LIU_SHA_PAIRS)
    if not sheng_qi:
        sheng_qi = list(SHENG_QI_PAIRS)
    ls = random.choice(liu_sha)
    sq = random.choice(sheng_qi)
    # Random order: 六煞+生气 or 生气+六煞
    if random.choice([True, False]):
        return ls + sq, ls, sq
    return sq + ls, ls, sq


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
        flash(get_translation('msg_login_required', get_current_language()), "error")
        return redirect(url_for('login'))
    user = User.query.filter_by(email=session['user']).first()

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
        if not user:
            flash(get_translation('msg_please_login', get_current_language()), "error")
            return redirect(url_for('login'))
        balance = get_usage_credit_balance(user)
        if balance < COST_NUMBER_ANALYSIS:
            msg = get_translation('msg_insufficient_credits', get_current_language()).format(cost=COST_NUMBER_ANALYSIS, balance=balance)
            flash(msg, "error")
            return redirect(url_for('index'))
        if not deduct_usage_credits(user.id, COST_NUMBER_ANALYSIS, 'number_analysis', reference_id=input_data[:50]):
            flash(get_translation('msg_credit_deduction_failed', get_current_language()), "error")
            return redirect(url_for('index'))

        # Analyze number
        primary_result, pair_stats, grouped_stats, grouped_energy, ending_warning, group_to_pairs, detailed_group_rows = analyze_number_pairs(input_data)
        
        # Save to history
        if user:
            existing_history = UserHistory.query.filter_by(
                user_id=user.id, 
                input_data=input_data
            ).first()
            if not existing_history:
                new_history = UserHistory(user_id=user.id, input_data=input_data)
                db.session.add(new_history)
                user_histories = UserHistory.query.filter_by(user_id=user.id).order_by(UserHistory.created_at.desc()).all()
                if len(user_histories) > 10:
                    for old_history in user_histories[10:]:
                        db.session.delete(old_history)
                db.session.commit()

        # Show advanced features for this analysis (user already paid 2 credits)
        secondary_result = perform_secondary_check(input_data)
        special_definitions = check_special_conditions(primary_result)
        profile_list = []
        for group, data in grouped_stats.items():
            if group in energy_descriptions:
                profile_list.append((group, energy_descriptions[group], data['percent']))
        profile_list.sort(key=lambda x: x[2], reverse=True)
        sorted_profiles = profile_list

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
                           user=session.get('user'),
                           credit_balance=get_usage_credit_balance(user) if user else 0)


@app.route('/ai')
def ai_page():
    """AI chat page. Each request costs 3 credits."""
    if not session.get('user'):
        return redirect(url_for('login'))
    try:
        from gemini_service import is_available as gemini_is_available
        gemini_available = gemini_is_available()
    except Exception:
        gemini_available = False
    return render_template('ai.html', gemini_available=gemini_available)


@app.route('/ask_ai', methods=['POST'])
def ask_ai():
    """Ask Gemini about a number/car plate. Costs 3 credits per request."""
    if not session.get('user'):
        return jsonify({'error': 'Login required'}), 401
    user = User.query.filter_by(email=session['user']).first()
    if not user:
        return jsonify({'error': 'User not found'}), 401
    balance = get_usage_credit_balance(user)
    if balance < COST_AI_REQUEST:
        err_msg = get_translation('msg_insufficient_credits', get_current_language()).format(cost=COST_AI_REQUEST, balance=balance)
        return jsonify({'error': err_msg}), 402
    if not deduct_usage_credits(user.id, COST_AI_REQUEST, 'ai_request', reference_id=None):
        return jsonify({'error': get_translation('msg_credit_deduction_failed', get_current_language())}), 402
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

    email = password = phone = None  # always declared

    if request.is_json:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        phone = data.get('phone')
    else:
        email = request.form.get('email')
        password = request.form.get('password')
        phone = (request.form.get('phone') or '').strip()

    if not email or not password:
        if request.is_json:
            return jsonify({'message': 'Email and password are required'}), 400
        else:
            flash(get_translation('msg_email_password_required', get_current_language()), "error")
            return redirect(url_for('register'))

    ref_for_redirect = (request.form.get('ref') or request.args.get('ref') or '').strip()[:20]
    phone_normalized = _normalize_phone_e164(phone) if phone else ''
    if not phone_normalized or len(phone_normalized) < 10:
        if request.is_json:
            return jsonify({'message': 'Valid WhatsApp number is required'}), 400
        flash(get_translation('msg_phone_required', get_current_language()), 'error')
        return redirect(url_for('register', ref=ref_for_redirect) if ref_for_redirect else url_for('register'))

    # Check duplicate phone (one account per WhatsApp number)
    for u in User.query.filter(User.phone.isnot(None)).filter(User.phone != '').all():
        if _normalize_phone_e164(u.phone) == phone_normalized:
            if request.is_json:
                return jsonify({'message': 'This WhatsApp number is already registered'}), 400
            flash(get_translation('msg_phone_exists', get_current_language()), 'error')
            return redirect(url_for('register', ref=ref_for_redirect) if ref_for_redirect else url_for('register'))

    if User.query.filter_by(email=email).first():
        if request.is_json:
            return jsonify({'message': 'User already exists'}), 400
        else:
            flash(get_translation('msg_user_exists', get_current_language()), "error")
            return redirect(url_for('register', ref=ref_for_redirect) if ref_for_redirect else url_for('register'))

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Referral: ref can be in query (?ref=CODE) or session (set when landing with ref)
    ref_code = request.args.get('ref') or request.form.get('ref') or session.pop('referral_ref', None)
    referred_by_id = None
    if ref_code:
        referrer = User.query.filter_by(referral_code=ref_code.upper()).first()
        if referrer and referrer.email != email:
            referred_by_id = referrer.id

    now = datetime.utcnow()
    new_user = User(
        email=email, password=hashed_password, phone=phone_normalized, referred_by_id=referred_by_id,
        plan='free',
        credits_balance=CREDITS_FREE_PER_MONTH,
        credits_per_month=CREDITS_FREE_PER_MONTH,
        credit_reset_at=now + timedelta(days=30)
    )
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
        flash(get_translation('msg_register_success', get_current_language()), "success")
        return redirect(url_for('login'))



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = (request.form.get('email') or '').strip()
        password = request.form.get('password') or ''
        if not email or not password:
            flash(get_translation('msg_fill_email_password', get_current_language()), "error")
            return render_template('login.html')
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            session['user'] = email
            session['is_pro'] = (getattr(user, 'plan', None) in ('starter', 'pro', 'master', 'monthly', 'annual')) or user.is_pro
            session['is_admin'] = getattr(user, 'is_admin', False)
            return redirect(url_for('index'))
        flash(get_translation('msg_login_failed', get_current_language()), "error")
    return render_template('login.html')


def _normalize_phone_e164(phone):
    """Normalize to E.164 for Twilio (e.g. +60123456789)."""
    if not phone:
        return ''
    s = re.sub(r'\s+', '', phone.strip())
    if s.startswith('+'):
        return s
    if s.startswith('60'):
        return '+' + s
    if s.startswith('0'):
        return '+6' + s  # Malaysia
    return '+' + s


@app.route('/login/otp/request', methods=['POST'])
def login_otp_request():
    """Send WhatsApp OTP via Twilio Verify. Phone only — OTP is sent to WhatsApp."""
    phone = (request.form.get('phone') or '').strip()
    phone = _normalize_phone_e164(phone)
    if not phone or len(phone) < 10:
        flash(get_translation('msg_login_otp_phone_required', get_current_language()), 'error')
        return redirect(url_for('login', otp=1))
    # Find user by phone (match normalized)
    user = None
    for u in User.query.filter(User.phone.isnot(None)).filter(User.phone != '').all():
        if _normalize_phone_e164(u.phone) == phone:
            user = u
            break
    if not user:
        flash(get_translation('msg_login_otp_no_account', get_current_language()), 'error')
        return redirect(url_for('login', otp=1))
    sid = app.config.get('TWILIO_VERIFY_SERVICE_SID')
    auth = (app.config.get('TWILIO_ACCOUNT_SID') or '', app.config.get('TWILIO_AUTH_TOKEN') or '')
    if not sid or not auth[0] or not auth[1]:
        flash(get_translation('msg_login_otp_unavailable', get_current_language()), 'error')
        return redirect(url_for('login', otp=1))
    try:
        r = _requests.post(
            f'https://verify.twilio.com/v2/Services/{sid}/Verifications',
            auth=auth,
            data={'To': phone, 'Channel': 'whatsapp'},
            timeout=10
        )
        if r.status_code != 201:
            flash(get_translation('msg_login_otp_send_failed', get_current_language()), 'error')
            return redirect(url_for('login', otp=1))
    except Exception as e:
        if app.debug:
            print('Twilio Verify error:', e)
        flash(get_translation('msg_login_otp_send_failed', get_current_language()), 'error')
        return redirect(url_for('login', otp=1))
    session['otp_email'] = user.email
    session['otp_phone'] = phone
    flash(get_translation('msg_login_otp_sent', get_current_language()), 'success')
    return redirect(url_for('login', otp_verify=1))


@app.route('/login/otp/verify', methods=['POST'])
def login_otp_verify():
    """Verify OTP and log in; redirect to profile with set_password=1."""
    code = (request.form.get('code') or '').strip()
    email = session.get('otp_email')
    phone = session.get('otp_phone')
    if not code or not email or not phone:
        flash(get_translation('msg_login_otp_invalid', get_current_language()), 'error')
        return redirect(url_for('login', otp_verify=1))
    sid = app.config.get('TWILIO_VERIFY_SERVICE_SID')
    auth = (app.config.get('TWILIO_ACCOUNT_SID') or '', app.config.get('TWILIO_AUTH_TOKEN') or '')
    if not sid or not auth[0]:
        flash(get_translation('msg_login_otp_unavailable', get_current_language()), 'error')
        return redirect(url_for('login'))
    try:
        r = _requests.post(
            f'https://verify.twilio.com/v2/Services/{sid}/VerificationCheck',
            auth=auth,
            data={'To': phone, 'Code': code},
            timeout=10
        )
        if r.status_code != 200 or (r.json() or {}).get('status') != 'approved':
            flash(get_translation('msg_login_otp_invalid', get_current_language()), 'error')
            return redirect(url_for('login', otp_verify=1))
    except Exception as e:
        if app.debug:
            print('Twilio Verify check error:', e)
        flash(get_translation('msg_login_otp_invalid', get_current_language()), 'error')
        return redirect(url_for('login', otp_verify=1))
    user = User.query.filter_by(email=email).first()
    if not user:
        session.pop('otp_email', None)
        session.pop('otp_phone', None)
        return redirect(url_for('login'))
    if not user.phone or _normalize_phone_e164(user.phone) != phone:
        user.phone = phone
        db.session.commit()
    session['user'] = user.email
    session['is_pro'] = (getattr(user, 'plan', None) in ('starter', 'pro', 'master', 'monthly', 'annual')) or user.is_pro
    session['is_admin'] = getattr(user, 'is_admin', False)
    session.pop('otp_email', None)
    session.pop('otp_phone', None)
    flash(get_translation('msg_login_otp_success', get_current_language()), 'success')
    return redirect(url_for('profile', set_password='1'))


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
            flash(get_translation('msg_enter_email', lang), 'error')
            return redirect(url_for('forgot_password'))
        user = User.query.filter_by(email=email).first()
        if not user:
            # Don't reveal whether email exists
            flash(get_translation('msg_reset_sent', lang), 'success')
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
            flash(get_translation('msg_reset_email_sent', lang), 'success')
        else:
            flash(get_translation('msg_reset_failed', lang), 'error')
        return redirect(url_for('login'))
    return render_template('forgot_password.html')


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    t = PasswordResetToken.query.filter_by(token=token).first()
    if not t or t.used_at or t.expires_at < datetime.utcnow():
        flash(get_translation('msg_link_invalid', get_current_language()), 'error')
        return redirect(url_for('forgot_password'))
    if request.method == 'POST':
        password = request.form.get('password') or ''
        if len(password) < 6:
            flash(get_translation('msg_password_min', get_current_language()), 'error')
            return render_template('reset_password.html', token=token)
        user = t.user
        user.password = bcrypt.generate_password_hash(password).decode('utf-8')
        t.used_at = datetime.utcnow()
        db.session.commit()
        flash(get_translation('msg_password_updated', get_current_language()), 'success')
        return redirect(url_for('login'))
    return render_template('reset_password.html', token=token)


@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('is_pro', None)
    session.pop('is_admin', None)
    flash(get_translation('msg_logged_out', get_current_language()), "error")
    return redirect(url_for('login'))


def _get_lucky_history(user_id, limit=10):
    """Last N lucky numbers for user; favorites first, then by created_at desc. Returns id, number, created_at, is_favorite."""
    if not user_id:
        return []
    rows = LuckyNumberHistory.query.filter_by(user_id=user_id).order_by(
        LuckyNumberHistory.is_favorite.desc(),
        LuckyNumberHistory.created_at.desc()
    ).limit(limit).all()
    return [{'id': r.id, 'number': r.number, 'created_at': r.created_at, 'is_favorite': getattr(r, 'is_favorite', False)} for r in rows]


@app.route('/lucky', methods=['GET', 'POST'])
def lucky_number():
    """Lucky 4-digit generator. 1 credit per generation; history of last 10 (no category labels)."""
    mode = 'general'
    day_master = None
    user = None
    if session.get('user'):
        user = User.query.filter_by(email=session['user']).first()
        if user:
            day_master = getattr(user, 'day_master', None)

    if request.method == 'POST':
        if not user:
            flash(get_translation('msg_please_login', get_current_language()), 'error')
            return redirect(url_for('login'))
        balance = get_usage_credit_balance(user)
        if balance < COST_LUCKY_GENERATION:
            msg = get_translation('msg_insufficient_credits', get_current_language()).format(
                cost=COST_LUCKY_GENERATION, balance=balance
            )
            flash(msg, 'error')
            return redirect(url_for('lucky_number'))
        mode = request.form.get('mode', 'general')
        if mode == 'personal' and not day_master:
            flash(get_translation('lucky_set_day_master', get_current_language()), 'error')
            return redirect(url_for('lucky_number'))
        existing = LuckyNumberHistory.query.filter_by(user_id=user.id).all()
        if len(existing) >= 10 and all(getattr(r, 'is_favorite', False) for r in existing):
            flash(get_translation('lucky_all_fav_notification', get_current_language()), 'error')
            return redirect(url_for('lucky_number'))
        if not deduct_usage_credits(user.id, COST_LUCKY_GENERATION, 'lucky_generation', reference_id=None):
            flash(get_translation('msg_credit_deduction_failed', get_current_language()), 'error')
            return redirect(url_for('lucky_number'))
        number, _, _ = generate_lucky_4digit(mode=mode, day_master=day_master)
        db.session.add(LuckyNumberHistory(user_id=user.id, number=number, is_favorite=False))
        db.session.flush()
        all_rows = LuckyNumberHistory.query.filter_by(user_id=user.id).order_by(
            LuckyNumberHistory.is_favorite.asc(),
            LuckyNumberHistory.created_at.asc()
        ).all()
        while len(all_rows) > 10:
            to_remove = all_rows.pop(0)
            db.session.delete(to_remove)
        db.session.commit()
        history = _get_lucky_history(user.id)
        return render_template('lucky_number.html', generated=number, mode=mode, day_master=day_master, history=history)
    history = _get_lucky_history(user.id if user else None)
    return render_template('lucky_number.html', generated=None, mode=mode, day_master=day_master, history=history)


@app.route('/lucky/toggle-favorite/<int:entry_id>', methods=['POST'])
def lucky_toggle_favorite(entry_id):
    """Toggle is_favorite for a lucky number history entry. Returns JSON."""
    if not session.get('user'):
        return jsonify({'ok': False, 'error': 'Login required'}), 401
    user = User.query.filter_by(email=session['user']).first()
    if not user:
        return jsonify({'ok': False, 'error': 'Login required'}), 401
    entry = LuckyNumberHistory.query.filter_by(id=entry_id, user_id=user.id).first()
    if not entry:
        return jsonify({'ok': False, 'error': 'Not found'}), 404
    entry.is_favorite = not getattr(entry, 'is_favorite', False)
    db.session.commit()
    return jsonify({'ok': True, 'is_favorite': entry.is_favorite})


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if not session.get('user'):
        return redirect(url_for('login'))
    user = User.query.filter_by(email=session['user']).first()
    if not user:
        return redirect(url_for('login'))
    if request.method == 'POST':
        user.display_name = (request.form.get('display_name') or '').strip() or None
        raw_phone = (request.form.get('phone') or '').strip()
        user.phone = _normalize_phone_e164(raw_phone) if raw_phone and len(_normalize_phone_e164(raw_phone)) >= 10 else None
        dm = (request.form.get('day_master') or '').strip()
        if dm in ('木', '火', '土', '金', '水'):
            user.day_master = dm
        else:
            user.day_master = None
        db.session.commit()
        flash(get_translation('msg_profile_updated', get_current_language()), 'success')
        return redirect(url_for('profile'))
    set_password_prompt = request.args.get('set_password') == '1'
    mail_subscriber = getattr(user, 'mail_subscriber', False)
    # Referral data (for inline section on profile)
    if not user.referral_code:
        for _ in range(5):
            code = _generate_referral_code()
            if not User.query.filter_by(referral_code=code).first():
                user.referral_code = code
                db.session.commit()
                break
    share_url = request.url_root.rstrip('/') + url_for('register') + '?ref=' + (user.referral_code or '')
    referral_count = ReferralCreditGrant.query.filter_by(referrer_id=user.id).count()
    return render_template('profile.html', user=user,
                          credit_balance=get_usage_credit_balance(user),
                          credit_balance_cents=get_credit_balance_cents(user.id),
                          set_password_prompt=set_password_prompt, mail_subscriber=mail_subscriber,
                          share_url=share_url, referral_code=user.referral_code or '',
                          referral_count=referral_count, referral_bonus_cents=REFERRAL_BONUS_CENTS)


@app.route('/profile/subscribe_mail', methods=['POST'])
def profile_subscribe_mail():
    """Subscribe to mail service for +4 credits per month."""
    if not session.get('user'):
        return redirect(url_for('login'))
    user = User.query.filter_by(email=session['user']).first()
    if not user:
        return redirect(url_for('login'))
    user.mail_subscriber = True
    db.session.commit()
    flash(get_translation('msg_mail_subscribed', get_current_language()), 'success')
    return redirect(url_for('profile'))


@app.route('/profile/set_password', methods=['POST'])
def profile_set_password():
    """Set or update password (e.g. after OTP login); suggest saving in browser/password app."""
    if not session.get('user'):
        return redirect(url_for('login'))
    user = User.query.filter_by(email=session['user']).first()
    if not user:
        return redirect(url_for('login'))
    password = (request.form.get('password') or '').strip()
    if len(password) < 6:
        flash(get_translation('msg_password_min', get_current_language()), 'error')
        return redirect(url_for('profile', set_password='1'))
    user.password = bcrypt.generate_password_hash(password).decode('utf-8')
    db.session.commit()
    flash(get_translation('msg_password_updated', get_current_language()), 'success')
    return redirect(url_for('profile'))


@app.route('/clear_history', methods=['POST'])
def clear_history():
    if session.get('user'):
        user = User.query.filter_by(email=session['user']).first()
        if user:
            UserHistory.query.filter_by(user_id=user.id).delete()
            db.session.commit()
            flash(get_translation('msg_history_cleared', get_current_language()), "success")
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

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    # Business WhatsApp number (no + or spaces). Set WHATSAPP_BUSINESS_NUMBER in .env e.g. 60123456789
    whatsapp_number = (os.environ.get('WHATSAPP_BUSINESS_NUMBER') or '60123456789').strip().replace('+', '').replace(' ', '')
    if request.method == 'POST':
        services = request.form.getlist('services') or []
        message = (request.form.get('message') or '').strip()
        name = (request.form.get('name') or '').strip()
        email = (request.form.get('email') or '').strip()
        # Build structured message for WhatsApp
        lines = [get_translation('contact_wa_intro', get_current_language())]
        if services:
            lines.append('')
            lines.append(get_translation('contact_wa_services', get_current_language()) + ':')
            service_labels = {
                'change_phone': get_translation('contact_service_change_phone', get_current_language()),
                'change_car_plate': get_translation('contact_service_change_car_plate', get_current_language()),
                'read_bazi': get_translation('contact_service_read_bazi', get_current_language()),
                'house_fengshui': get_translation('contact_service_house_fengshui', get_current_language()),
            }
            for s in services:
                if s in service_labels:
                    lines.append('• ' + service_labels[s])
        if message:
            lines.append('')
            lines.append(get_translation('contact_wa_request', get_current_language()) + ':')
            lines.append(message)
        if name or email:
            lines.append('')
            if name:
                lines.append(get_translation('contact_wa_name', get_current_language()) + ': ' + name)
            if email:
                lines.append(get_translation('contact_wa_email', get_current_language()) + ': ' + email)
        text = '\n'.join(lines)
        from urllib.parse import quote
        encoded = quote(text, safe='')
        return redirect(f'https://wa.me/{whatsapp_number}?text={encoded}', code=302)
    return render_template('contact.html', whatsapp_number=whatsapp_number)

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
    """Apply store-credit DEBIT if used, mark voucher USED, set plan + grant usage credits, grant referrer credits."""
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
    user.plan = order.plan
    user.credits_per_month = CREDITS_BY_PLAN.get(order.plan, CREDITS_FREE_PER_MONTH)
    now = datetime.utcnow()
    extend_days = 30
    if not user.pro_until or user.pro_until < now:
        user.pro_until = now + timedelta(days=extend_days)
    else:
        user.pro_until += timedelta(days=extend_days)
    # First-month usage credits
    first_grant = user.credits_per_month
    user.credits_balance = (user.credits_balance or 0) + first_grant
    user.credit_reset_at = now + timedelta(days=30)
    db.session.add(UsageCreditEntry(
        user_id=user.id, type='monthly_grant', amount=first_grant,
        reference_type='subscription_start', reference_id=str(order.id)
    ))
    # Referrer usage-credit bonus (idempotent)
    if getattr(user, 'referred_by_id', None) and user.referred_by_id != user.id:
        existing = ReferralUsageCreditGrant.query.filter_by(
            referrer_id=user.referred_by_id, referred_user_id=user.id
        ).first()
        if not existing:
            bonus = (
                REFERRAL_CREDITS_WHEN_MASTER if order.plan == 'master' else
                REFERRAL_CREDITS_WHEN_PRO if order.plan == 'pro' else
                REFERRAL_CREDITS_WHEN_STARTER
            )
            referrer = User.query.get(user.referred_by_id)
            if referrer:
                referrer.credits_balance = (referrer.credits_balance or 0) + bonus
                db.session.add(UsageCreditEntry(
                    user_id=referrer.id, type='referral_bonus', amount=bonus,
                    reference_type='referral', reference_id=str(user.id)
                ))
                db.session.add(ReferralUsageCreditGrant(
                    referrer_id=user.referred_by_id, referred_user_id=user.id,
                    plan=order.plan, credits_granted=bonus
                ))
    order.status = 'paid'
    order.paid_at = now
    db.session.commit()

@app.route('/upgrade')
def upgrade_success():
    """Stripe success redirect: fulfill PendingOrder (credit/voucher), set is_pro."""
    session_id = request.args.get('session_id')
    if not session_id:
        if session.get('user'):
            flash(get_translation('msg_subscribe_success_short', get_current_language()), 'success')
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
    flash(get_translation('msg_subscribe_success', get_current_language()), 'success')
    return redirect(url_for('index'))

@app.route('/upgrade/<int:user_id>', methods=['POST'])
def upgrade(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    session['is_pro'] = True
    flash(get_translation('msg_upgrade_success', get_current_language()), "success")

    user.is_pro = True
    db.session.commit()

    return jsonify({'message': f'User {user.email} upgraded to paid'}), 200


@app.route('/subscribe/<plan>', methods=['GET', 'POST'])
def subscribe(plan):
    if plan not in PLAN_PRICE_CENTS:
        flash(get_translation('msg_invalid_subscription', get_current_language()), 'error')
        return redirect(url_for('pricing'))
    base_cents = PLAN_PRICE_CENTS[plan]
    price_id = STRIPE_PRICE_IDS.get(plan)
    if not STRIPE_PRICE_IDS.get(plan):
        pass  # we use price_data with unit_amount, so price_id optional

    if not session.get('user'):
        flash(get_translation('msg_please_login', get_current_language()), 'error')
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
        flash(get_translation('msg_use_balance_done', get_current_language()), 'success')
        return redirect(url_for('index'))

    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'myr',
                'unit_amount': final_cents,
                'product_data': {
                    'name': {'starter': 'Starter 150 credits/mo', 'pro': 'Pro 500 credits/mo', 'master': 'Master Unlimited'}.get(plan, plan),
                    'description': 'Numerology analysis · Number 2 credits/use, AI 3 credits/use'
                },
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=YOUR_DOMAIN + '/upgrade?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=YOUR_DOMAIN + '/pricing',
        customer_email=session.get('user'),
        metadata={'pending_order_id': str(order.id), 'plan': plan}
    )
    order.stripe_session_id = checkout_session.id
    db.session.commit()
    return redirect(checkout_session.url, code=303)



@app.route('/pay')
def pay():
    """Legacy one-off pay: redirects to Starter plan price."""
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'myr',
                'unit_amount': PLAN_PRICE_CENTS['starter'],
                'product_data': {
                    'name': 'Starter 150 credits/mo',
                    'description': 'Numerology analysis · 150 credits/month'
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

    # One-time checkout completed (our subscribe flow uses mode='payment')
    if event['type'] == 'checkout.session.completed':
        session_obj = event['data']['object']
        order_id = session_obj.get('metadata', {}).get('pending_order_id')
        if order_id:
            try:
                order = PendingOrder.query.get(int(order_id))
                if order and order.status == 'pending':
                    _fulfill_order(order)
            except (ValueError, TypeError):
                pass

    # Subscription invoice (if you add subscription mode later)
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
            if getattr(user, 'referred_by_id', None) and user.referred_by_id != user.id:
                existing = ReferralCreditGrant.query.filter_by(
                    referrer_id=user.referred_by_id, referred_user_id=user.id
                ).first()
                if not existing:
                    db.session.add(CreditLedgerEntry(
                        user_id=user.referred_by_id, type='CREDIT', amount_cents=REFERRAL_BONUS_CENTS,
                        reference_type='referral', reference_id=str(user.id), note='Referral bonus'
                    ))
                    db.session.add(ReferralCreditGrant(
                        referrer_id=user.referred_by_id, referred_user_id=user.id, amount_cents=REFERRAL_BONUS_CENTS
                    ))
            db.session.commit()

    return jsonify({'status': 'success'}), 200



if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8050)