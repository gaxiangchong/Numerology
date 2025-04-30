
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User
from extensions import db, migrate  # ✅ NEW
from flask_bcrypt import Bcrypt

import stripe, json

# Replace with your real test keys
stripe.api_key = "sk_test_51REvA7P2st6SZBP1tb42aLKfEAYH0P4K9Q1Q9ayAAlmU6tITilb4Qs9lqxXYGGFYUpMbTjdfVfqUdRwF55NOak1500fDtgP4D4"  # SECRET KEY

YOUR_DOMAIN = "http://127.0.0.1:5000"

app = Flask(__name__)


""" from flask_migrate import Migrate
migrate = Migrate(app, db) """

app.secret_key = 'your_secret_key'  # Needed for sessions

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
bcrypt = Bcrypt(app)

migrate.init_app(app, db)

# Mock database (you can switch to SQLite later)
users = {
    "test@example.com": {
        "password": generate_password_hash("123456"),
        "is_pro": True,
        "pro_until": None,  # Optional
        "referrals": 0
    }
}

with app.app_context():
    db.create_all()


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
        "优点": "天资聪明，心地善良，善解人意，喜欢帮助别人，单纯，事业有成，代天行医，福报好，财运好。",
        "缺点": "心胸较小，容易受他人影响，单纯容易被欺骗。",
        "事业": "适合做医生、心理学、艺术、宗教事业等。",
        "健康": "容易出现血液、血循环、心脑血管等问题。"
    },
    "生气": {
        "title": "生气磁场",
        "优点": "开朗、乐观、随缘、活力四射，情感丰富，喜欢与人交往，和人相处融洽。",
        "缺点": "缺乏主见，容易受到外界影响，过于乐观，容易被欺骗。",
        "事业": "适合服务行业、财务、文化产业等。",
        "健康": "容易多胃病、心脏病、精神病等。"
    },
    "延年": {
        "title": "延年磁场",
        "优点": "有领导力，有责任心，敢于承担，心地善良，长寿。",
        "缺点": "女性强势，男性大男子主义，固执，缺乏变通。",
        "事业": "适合主导性、专业能力强的工作，求财平稳。",
        "健康": "心脏病、精神病、颈椎病、肩周炎等。"
    },
    "伏位": {
        "title": "伏位磁场",
        "优点": "耐性强、毅力大，具备潜力，善于推理逻辑，顾家。",
        "缺点": "不善随机应变，固执，处理事情反复琢磨，缺乏安全感。",
        "事业": "适合慢工细活、研究分析类工作，稳定行业。",
        "健康": "脑部问题、头痛、失眠、心脏病等。"
    },
    "祸害": {
        "title": "祸害磁场",
        "优点": "口才好，能言善道，八面玲珑，口吐莲花，喜好享受美食，口才带来财富。",
        "缺点": "直言直语，脾气急躁，气场暴躁，爱顶嘴，有点好强，爱抱怨，做事稍显粗心，感情易过度。",
        "事业": "讲师、教育、销售、律师、业务员、餐饮、娱乐、表演等行业容易被捧。适合从事与口才相关的工作。",
        "健康": "车祸、意外、体质差、抗力差、咽喉和口腔呼吸系统疾病。"
    },
    "六煞": {
        "title": "六煞磁场",
        "优点": "眼光远大，社交能力强，思维细腻，情感丰富，善于沟通，喜欢交往，艺术方面有独特的优势，吸引力强，异性缘佳，初见时给人深刻印象。",
        "缺点": "心思过于细腻，缺乏坚定的情感，易受他人影响，情绪不稳定，容易冲动。",
        "事业": "美容、艺术、医疗、服务行业和性别相关行业等；人际关系好但不易留住，因为不适合固定工作。",
        "健康": "肠胃病、皮肤病、抑郁症、失眠等。"
    },
    "绝命": {
        "title": "绝命磁场",
        "优点": "头脑反应快，记忆力好，能赚钱，目标明确，超强的判断力，善良、正义、胆子大，获取财富方面有优势，金钱观念强。",
        "缺点": "脾气差，中动暴躁，易走极端，不圆滑，心软，耳根子软，易相信朋友，容易与上层领导发生矛盾。",
        "事业": "不适合上班，适合做自己的行业，房地产、金融、股市等，早九晚五不适合，能赚钱也容易破产。",
        "健康": "免疫力低，容易得大病，肝肾疾病，积劳成疾，糖尿病等。"
    },
    "五鬼": {
        "title": "五鬼磁场",
        "优点": "才华横溢，高智商，想法多，鬼点子多，待人热情，处事果断，对技能掌握有深度，学习能力强，多才多艺，善于创意和战略，做事出其不意。",
        "缺点": "内心忧郁，喜欢特立独行，偷懒摸索，想法多反复无常，不走正道，久难以提振，不容易被别人看穿，缺乏安全感。",
        "事业": "宗教事业、企业续校、贸易公司、偏门生意，经营活动时间长常加班工作，容易撞正业，失业，缺乏中心稳定。",
        "健康": "如肝、肺、肾、老年脑病、心脏病、免疫力低、中风等。"
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

        has_removed_zero = False
        has_removed_five = False
        if len(original_indices_in_full_number) >= 2:
            has_removed_zero = any(idx in removed_zeros for idx in range(original_indices_in_full_number[0] + 1, original_indices_in_full_number[1]))
            has_removed_five = any(idx in removed_fives for idx in range(original_indices_in_full_number[0] + 1, original_indices_in_full_number[1]))

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

            if has_removed_zero:
                definition += '(隐)'
            if has_removed_five:
                definition += '(显)'

            pairs.append(definition)
            mapped_only.append(pair_mappings[pair])

            # Stats for group rows
            group_to_pairs[base_type].append(pair)
            try:
                level = pair_mappings[pair].split('[')[-1].replace(']', '')
                level_int = int(level)
                energy_score = max(0, 100 - (level_int - 1) * 25)
            except:
                energy_score = 0

            detailed_group_rows.append({
                'group': base_type,
                'pair': pair,
                'energy': f"{energy_score}%"
            })
        else:
            pairs.append(pair)

    # Frequency stats
    frequency = dict(Counter(mapped_only))
    total_mapped = sum(frequency.values())

    percentage = {}
    group_summary = defaultdict(int)
    energy_score_by_group = defaultdict(list)

    for key, count in frequency.items():
        base_type = key.split('[')[0]
        level = key.split('[')[-1].replace(']', '')

        try:
            level_int = int(level)
            energy_score = max(0, 100 - (level_int - 1) * 25)
        except:
            energy_score = 0

        percentage[key] = {
            'count': count,
            'percent': round((count / total_mapped) * 100, 1) if total_mapped > 0 else 0,
            'energy': f"{energy_score * count}%"
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

    # Ending warning logic
    last_pair = mapped_only[-1] if mapped_only else None
    ending_warning = None

    if last_pair:
        group_name = last_pair.split('[')[0]
        ending_warning = ending_financial_warnings.get(group_name)

    return pairs, percentage, grouped_percentage, grouped_energy_percent, ending_warning, group_to_pairs, detailed_group_rows



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


@app.route('/', methods=['GET', 'POST'])
def index():

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
                           is_pro=session.get('is_pro', False),
                           user=session.get('user'))




@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    email = password = user_type = None  # ✅ always declared

    if request.is_json:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        user_type = data.get('user_type', 'free')
    else:
        email = request.form.get('email')
        password = request.form.get('password')
        user_type = request.form.get('user_type', 'free')

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

    new_user = User(email=email, password_hash=hashed_password, user_type=user_type)
    db.session.add(new_user)
    db.session.commit()

    if request.is_json:
        return jsonify({'message': 'User registered successfully', 'user_type': new_user.user_type}), 201
    else:
        flash("注册成功，请登录", "success")
        return redirect(url_for('login'))



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = users.get(email)

        if user and check_password_hash(user['password'], password):
            session['user'] = email
            session['is_pro'] = user.get('is_pro', False)  # ✅ set correctly here
            return redirect(url_for('index'))
        else:
            flash("登录失败，请检查邮箱或密码", "error")
    return render_template('login.html')



@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("已登出", "info")
    return redirect(url_for('index'))

@app.route('/pricing')
def pricing():
    return render_template('pricing.html')

""" @app.route('/upgrade')
def upgrade():
    if session.get('user'):
        users[session['user']]['is_pro'] = True
        flash("您已升级为专业版用户！", "success")
    return redirect(url_for('index')) """

@app.route('/upgrade/<int:user_id>', methods=['POST'])
def upgrade(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    session['is_pro'] = True
    flash("您已成功订阅高级版！", "success")

    user.user_type = 'paid'
    db.session.commit()

    return jsonify({'message': f'User {user.email} upgraded to paid'}), 200


@app.route('/subscribe/<plan>')
def subscribe(plan):
    # Replace with your real Stripe price IDs
    price_lookup = {
        'monthly': 'price_1RJd0WP2st6SZBP1PfnZzp0O',  # ← replace with your monthly price ID
        'annual': 'price_1RJd0oP2st6SZBP1VzVFn81M'   # ← replace with your annual price ID
    }

    price_id = price_lookup.get(plan)
    if not price_id:
        return "无效的订阅类型", 400

    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': price_id,
            'quantity': 1,
        }],
        mode='subscription',
        success_url=YOUR_DOMAIN + '/upgrade?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=YOUR_DOMAIN + '/pricing',
        customer_email=session.get('user')  # Optional: pre-fill email if available
    )

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
                    'name': '升级为专业版',
                    'description': '解锁高级分析功能'
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
    endpoint_secret = 'whsec_...'  # 🔐 replace with your webhook secret from Stripe

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError as e:
        return jsonify({'error': 'Invalid payload'}), 400
    except stripe.error.SignatureVerificationError:
        return jsonify({'error': 'Invalid signature'}), 400

    # 🎯 Handle successful payment (subscription or renewal)
    if event['type'] == 'invoice.paid':
        invoice = event['data']['object']
        subscription_id = invoice['subscription']
        customer_email = invoice['customer_email']

        user = User.query.filter_by(email=customer_email).first()
        if user:
            user.is_pro = True
            user.stripe_subscription_id = subscription_id
            extend_days = 30  # You can adjust this based on pricing logic

            if not user.pro_until or user.pro_until < datetime.utcnow():
                user.pro_until = datetime.utcnow() + timedelta(days=extend_days)
            else:
                user.pro_until += timedelta(days=extend_days)

            db.session.commit()

    return jsonify({'status': 'success'}), 200



if __name__ == '__main__':
    app.run(debug=True)