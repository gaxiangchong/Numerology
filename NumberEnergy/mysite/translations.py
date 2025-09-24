# translations.py - Translation system for English and Chinese

# Translation dictionaries
TRANSLATIONS = {
    'en': {
        # Navigation
        'nav_home': 'Home',
        'nav_pricing': 'Pricing',
        'nav_contact': 'Contact',
        'nav_login': 'Login',
        'nav_logout': 'Logout',
        'nav_register': 'Register',
        
        # App titles and headers
        'app_title': 'Numerology Analysis Tool',
        'main_title': '✨ Numerology Analysis ✨',
        'contact_title': 'Contact Us',
        'pricing_title': 'Choose Your Perfect Plan',
        'login_title': 'Login',
        'register_title': 'Create Account',
        
        # Common elements
        'logo_text': 'Numerology Tool',
        'pro_badge': 'PRO',
        'free_badge': 'Free',
        'current_plan': 'Current Plan',
        'most_popular': 'Most Popular',
        'best_value': 'Best Value',
        
        # Buttons and actions
        'btn_analyze': 'Analyze',
        'btn_login': 'Login',
        'btn_register': 'Register',
        'btn_logout': 'Logout',
        'btn_subscribe': 'Subscribe',
        'btn_get_started': 'Get Started',
        'btn_contact': 'Contact Us',
        'btn_clear_history': 'Clear History',
        'btn_upgrade': 'Upgrade to Pro',
        'btn_test_upgrade': 'Test Upgrade Pro',
        'confirm_clear_history': 'Are you sure you want to clear all history?',
        
        # Form labels and inputs
        'input_label': 'Enter your license plate, phone number, or any English/number combination:',
        'email_label': 'Email:',
        'password_label': 'Password:',
        'input_placeholder': 'Enter your data here...',
        
        # Analysis results
        'your_input': 'Your Input:',
        'energy_analysis': 'Combination Energy Analysis:',
        'distribution_chart': 'Combination Type Distribution Chart',
        'recent_numbers': 'Recent Numbers',
        'no_history': 'No history available',
        'energy_warning': 'Financial Warning',
        'master_analysis': 'Master Analysis',
        'secondary_insights': 'Secondary Combination Insights:',
        'special_warnings': 'Special Combination Warnings:',
        'detailed_analysis': 'Detailed Magnetic Field Analysis',
        'personality_traits': 'Personality Traits',
        'career_insights': 'Career',
        'health_insights': 'Health',
        'advantages': 'Advantages',
        'disadvantages': 'Disadvantages',
        
        # Pricing page
        'pricing_subtitle': 'Unlock the power of numerology analysis with our comprehensive feature sets',
        'special_offer': 'Special Offer:',
        'new_user_trial': 'New users get 14 days free trial! Refer friends for 3 extra months.',
        'feature_comparison': 'Features',
        'free_plan': 'Free Plan',
        'master_monthly': 'Master Monthly',
        'master_annual': 'Master Annual',
        'perfect_for_starting': 'Perfect for getting started with numerology',
        'unlock_all_features': 'Unlock all advanced features',
        'maximum_savings': 'Maximum savings with all features',
        'free_forever': 'Free / forever',
        'per_month': '/ month',
        'per_year': '/ year',
        'save_amount': 'Save {amount} (was {original})',
        'save_percentage': 'Save {percentage} (was {original})',
        'two_months_free': 'Save {amount} (2 months free)',
        
        # Features
        'feature_basic_analysis': 'Basic Number Analysis',
        'feature_energy_charts': 'Energy Distribution Charts',
        'feature_history': 'Analysis History',
        'feature_mobile': 'Mobile Responsive',
        'feature_support': 'WhatsApp Support',
        'feature_unlimited': 'Unlimited Analysis',
        'feature_advanced_analysis': 'Advanced Magnetic Field Analysis',
        'feature_secondary_insights': 'Secondary Combination Insights',
        'feature_special_warnings': 'Special Combination Warnings',
        'feature_personality': 'Detailed Personality Profiles',
        'feature_career_health': 'Career & Health Insights',
        'feature_recommendations': 'Personalized Recommendations',
        'feature_priority_support': 'Priority WhatsApp Support',
        'feature_early_access': 'Early Access to New Features',
        'feature_extended_history': 'Extended Analysis History',
        'feature_export': 'Advanced Export Options',
        'feature_exclusive_reports': 'Exclusive Numerology Reports',
        'feature_guarantee': '30-day Money-back Guarantee',
        
        # Contact page
        'contact_subtitle': 'Have questions or need help? We\'re here to serve you!',
        'whatsapp_contact': 'WhatsApp Contact',
        'whatsapp_description': 'Contact us directly via WhatsApp for instant replies',
        'send_whatsapp': 'Send WhatsApp Message',
        'contact_info': 'Contact Information',
        'service_content': 'Service Content',
        'business_hours': 'Business Hours: 9:00 AM - 6:00 PM',
        'faq_title': 'Frequently Asked Questions',
        'faq_upgrade': 'How to upgrade to Master plan?',
        'faq_accuracy': 'Is numerology analysis accurate?',
        'faq_number_types': 'What types of numbers can be analyzed?',
        'faq_upgrade_answer': 'Click the "Pricing" button on the page, choose a subscription plan that suits you, or contact us via WhatsApp for more information.',
        'faq_accuracy_answer': 'Our analysis is based on traditional numerology theories, for reference only. We recommend combining with actual situations and personal judgment.',
        'faq_types_answer': 'Supports analysis of phone numbers, license plates, ID numbers, birthdays, and any number combinations.',
        
        # FAQ
        'faq_difference': 'What\'s the difference between Free and Master plans?',
        'faq_difference_answer': 'Free plan includes basic number analysis and charts. Master plan unlocks advanced magnetic field analysis, personality profiles, career insights, and personalized recommendations.',
        'faq_upgrade_downgrade': 'Can I upgrade or downgrade anytime?',
        'faq_upgrade_downgrade_answer': 'Yes! You can upgrade to Master plan anytime. Downgrading will take effect at your next billing cycle. Annual subscribers get prorated refunds.',
        'faq_trial': 'Is there a free trial for Master plans?',
        'faq_trial_answer': 'Yes! New users get 14 days free trial for Master features. No credit card required to start your trial.',
        'faq_payment': 'What payment methods do you accept?',
        'faq_payment_answer': 'We accept all major credit cards, PayPal, and bank transfers. All payments are processed securely through Stripe.',
        
        # Messages
        'upgrade_banner': 'Want to see more auxiliary analysis? <a href="/pricing" class="text-blue-400 underline">Upgrade to Master Plan</a>!',
        'welcome_back': 'Welcome Back',
        'welcome_message': 'Enter your account to continue using the analysis tool.',
        'no_account': 'Don\'t have an account? <a href="/register" class="text-blue-400 hover:underline">Click to register</a>',
        # REMOVED FOR TESTING - Pro account text completely hidden
        # 'need_pro': 'Need Pro account? <a href="/create_pro_account" class="text-green-400 hover:underline">Create Pro test account</a>',
        # 'need_pro': 'Need Pro account? <span class="text-gray-500">Create Pro test account (disabled for testing)</span>',
        'already_have_account': 'Already have an account? <a href="/login" class="text-blue-400 hover:underline">Click to login</a>',
        'currently_using': 'Currently Using',
        'get_started_free': 'Get Started Free',
        'start_monthly': 'Start Monthly Plan',
        'start_annual': 'Start Annual Plan',
        'free_registration': 'Free Registration',
        'subscribe_now': 'Subscribe Now',
        
        # Table headers
        'combination_type': 'Combination Type',
        'number_combination': 'Number Combination',
        'total_energy': 'Total Energy',
        'appearance_count': 'Appearance Count',
        
        # Service content
        'service_numerology': 'Numerology Analysis Consultation',
        'service_master': 'Master Plan Feature Explanation',
        'service_technical': 'Technical Support',
        'service_account': 'Account Related Issues',
    },
    
    'zh': {
        # Navigation
        'nav_home': '主页',
        'nav_pricing': '购买',
        'nav_contact': '联系我们',
        'nav_login': '登录',
        'nav_logout': '登出',
        'nav_register': '注册',
        
        # App titles and headers
        'app_title': '命理分析工具',
        'main_title': '✨奇门数字分析✨',
        'contact_title': '联系我们',
        'pricing_title': '选择适合你的计划',
        'login_title': '登录',
        'register_title': '创建账号',
        
        # Common elements
        'logo_text': '命理工具',
        'pro_badge': 'PRO',
        'free_badge': 'Free',
        'current_plan': '当前计划',
        'most_popular': '最受欢迎',
        'best_value': '最佳价值',
        
        # Buttons and actions
        'btn_analyze': '分析',
        'btn_login': '登录',
        'btn_register': '注册',
        'btn_logout': '登出',
        'btn_subscribe': '订阅',
        'btn_get_started': '开始使用',
        'btn_contact': '联系我们',
        'btn_clear_history': '清除历史',
        'btn_upgrade': '升级为大师版',
        'btn_test_upgrade': '测试升级Pro',
        'confirm_clear_history': '确定要清除所有历史记录吗？',
        
        # Form labels and inputs
        'input_label': '请输入您的车牌、电话号码、或任何英文、数字：',
        'email_label': '邮箱：',
        'password_label': '密码：',
        'input_placeholder': '在此输入您的数据...',
        
        # Analysis results
        'your_input': '您的输入内容：',
        'energy_analysis': '组合能量分析：',
        'distribution_chart': '组合类型分布图',
        'recent_numbers': '最近输入的数字',
        'no_history': '暂无历史记录',
        'energy_warning': '破财警示',
        'master_analysis': '大师分析',
        'secondary_insights': '辅助组合提示：',
        'special_warnings': '特殊组合提醒：',
        'detailed_analysis': '详细磁场分析',
        'personality_traits': '性格特点',
        'career_insights': '事业',
        'health_insights': '健康',
        'advantages': '优点',
        'disadvantages': '缺点',
        
        # Pricing page
        'pricing_subtitle': '通过我们全面的功能集解锁数字能量分析的力量',
        'special_offer': '特别优惠：',
        'new_user_trial': '新用户可免费试用 14 天！推荐好友可额外获得 3 个月奖励。',
        'feature_comparison': '功能对比',
        'free_plan': '基础版',
        'master_monthly': '大师版 - 月付',
        'master_annual': '大师版 - 年付',
        'perfect_for_starting': '适合开始使用命理学',
        'unlock_all_features': '解锁所有高级功能',
        'maximum_savings': '最大节省，包含所有功能',
        'free_forever': '免费 / 永久',
        'per_month': '/ 月',
        'per_year': '/ 年',
        'save_amount': '节省 {amount}，原价 {original}',
        'save_percentage': '节省 {percentage}，原价 {original}',
        'two_months_free': '节省 {amount}，相当于 2 个月免费',
        
        # Features
        'feature_basic_analysis': '基础数字分析',
        'feature_energy_charts': '能量分布图表',
        'feature_history': '分析历史',
        'feature_mobile': '移动响应式',
        'feature_support': 'WhatsApp 支持',
        'feature_unlimited': '无限分析',
        'feature_advanced_analysis': '高级磁场分析',
        'feature_secondary_insights': '辅助组合洞察',
        'feature_special_warnings': '特殊组合警告',
        'feature_personality': '详细性格档案',
        'feature_career_health': '事业与健康洞察',
        'feature_recommendations': '个性化推荐',
        'feature_priority_support': '优先 WhatsApp 支持',
        'feature_early_access': '新功能早期访问',
        'feature_extended_history': '扩展分析历史',
        'feature_export': '高级导出选项',
        'feature_exclusive_reports': '独家命理报告',
        'feature_guarantee': '30天退款保证',
        
        # Contact page
        'contact_subtitle': '有任何问题或需要帮助？我们随时为您服务！',
        'whatsapp_contact': 'WhatsApp 联系',
        'whatsapp_description': '通过 WhatsApp 直接联系我们，获得即时回复',
        'send_whatsapp': '发送 WhatsApp 消息',
        'contact_info': '联系方式',
        'service_content': '服务内容',
        'business_hours': '营业时间: 9:00 AM - 6:00 PM',
        'faq_title': '常见问题',
        'faq_upgrade': '如何升级到大师版？',
        'faq_accuracy': '数字能量分析准确吗？',
        'faq_number_types': '可以分析哪些类型的数字？',
        'faq_upgrade_answer': '点击页面上的"购买"按钮，选择适合您的订阅计划，或通过 WhatsApp 联系我们获取更多信息。',
        'faq_accuracy_answer': '我们的分析基于传统命理学理论，仅供参考。建议结合实际情况和个人判断使用。',
        'faq_types_answer': '支持电话号码、车牌号码、身份证号码、生日等任何数字组合的分析。',
        
        # FAQ
        'faq_difference': '免费版和大师版有什么区别？',
        'faq_difference_answer': '免费版包括基础数字分析和图表。大师版解锁高级磁场分析、性格档案、事业洞察和个性化推荐。',
        'faq_upgrade_downgrade': '可以随时升级或降级吗？',
        'faq_upgrade_downgrade_answer': '是的！您可以随时升级到大师版。降级将在下一个计费周期生效。年度订阅者获得按比例退款。',
        'faq_trial': '大师版有免费试用吗？',
        'faq_trial_answer': '是的！新用户获得大师功能的14天免费试用。开始试用无需信用卡。',
        'faq_payment': '接受哪些支付方式？',
        'faq_payment_answer': '我们接受所有主要信用卡、PayPal和银行转账。所有支付都通过Stripe安全处理。',
        
        # Messages
        'upgrade_banner': '要查看更多辅助分析？<a href="/pricing" class="text-blue-400 underline">升级为大师版</a>！',
        'welcome_back': '欢迎回来',
        'welcome_message': '输入您的账号以继续使用分析工具。',
        'no_account': '还没有账号？<a href="/register" class="text-blue-400 hover:underline">点击注册</a>',
        # REMOVED FOR TESTING - Pro account text completely hidden
        # 'need_pro': '需要Pro账户？<a href="/create_pro_account" class="text-green-400 hover:underline">创建Pro测试账户</a>',
        # 'need_pro': '需要Pro账户？<span class="text-gray-500">创建Pro测试账户 (测试时已禁用)</span>',
        'already_have_account': '已有账号？<a href="/login" class="text-blue-400 hover:underline">点击登录</a>',
        'currently_using': '当前已使用',
        'get_started_free': '免费开始',
        'start_monthly': '开始月度计划',
        'start_annual': '开始年度计划',
        'free_registration': '免费注册',
        'subscribe_now': '立即订阅',
        
        # Table headers
        'combination_type': '组合类型',
        'number_combination': '数字组合',
        'total_energy': '累计能量',
        'appearance_count': '出现次数',
        
        # Service content
        'service_numerology': '数字能量分析咨询',
        'service_master': '大师版功能说明',
        'service_technical': '技术问题支持',
        'service_account': '账户相关问题',
    }
}

def get_translation(key, language='en'):
    """Get translation for a key in the specified language"""
    return TRANSLATIONS.get(language, {}).get(key, key)

def get_current_language():
    """Get current language from session or default to English"""
    from flask import session
    return session.get('language', 'en')

def set_language(language):
    """Set language in session"""
    from flask import session
    session['language'] = language
