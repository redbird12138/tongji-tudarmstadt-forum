# ============== 不要在这里放饮食需求代码 ==============
# 文件开头是导入和配置部分
import streamlit as st
import pandas as pd
from datetime import datetime
import json
import os
import hashlib
import io

# 页面配置
st.set_page_config(
    page_title="International Forum System",
    page_icon="🎓",
    layout="wide"
)

# 管理员密码
ADMIN_PASSWORD = "tongji2025"

# ============== 1. 首先更新LANGUAGES字典 ==============
# 语言配置 - 用这个完整版本替换原有的LANGUAGES字典
LANGUAGES = {
    "en": {
        "title": "International Forum of Graduate Students on Mechanics of Smart Materials",
        "subtitle": "Shanghai, China | October 13-15, 2025",
        "paper_title": "Paper Title",
        "author_name": "Author Name",
        "author_affiliation": "Affiliation",
        "add_author": "Add Another Author",
        "remove_author": "Remove",
        "is_presenting": "Presenting Author",
        "is_corresponding": "Corresponding Author",
        "authors_help": "Add all authors with their affiliations and roles",
        "session": "Session",
        "abstract": "Abstract",
        "abstract_help": "Please provide a detailed abstract of your research or upload an abstract file",
        "abstract_upload": "Upload Abstract File",
        "download_template": "Download Template",
        "accommodation": "Accommodation Dates",
        "accommodation_help": "Select specific nights you need accommodation during the conference period (for overseas participants only)",
        "full_name": "Full Name",
        "passport_number": "Passport Number",
        "accommodation_info": "Personal Information for Accommodation",
        "custom_dates": "Other dates (please specify):",
        "dietary_requirements": "Dietary Requirements",
        "dietary_help": "Please specify any dietary requirements (for catering during the conference)",
        "dietary_vegan": "Vegan",
        "dietary_vegetarian": "Vegetarian", 
        "dietary_none": "No special requirements",
        "dietary_other": "Other (please specify)",
        "dietary_specify": "Please specify your dietary requirements:",
        "contact_email": "Contact Email",
        "contact_phone": "Contact Phone (Optional)",
        "submit": "Submit Submission",
        "reset": "Reset Form",
        "success": "🎉 Submission successful! We will contact you soon.",
        "error": "❌ Please fill in all required fields",
        "language": "Language",
        "my_submissions": "📋 My Submissions",
        "search_submissions": "🔍 Search My Submissions",
        "email_placeholder": "Enter your email to view submissions",
        "search": "Search",
        "no_submissions": "No submissions found for this email address.",
        "admin_panel": "🛠️ Admin Panel",
        "admin_login": "Admin Login",
        "admin_password": "Admin Password",
        "login": "Login",
        "logout": "Logout",
        "invalid_password": "❌ Invalid password",
        "file_uploaded": "✅ File uploaded successfully",
        "file_error": "❌ Error uploading file",
        "sessions": [
            "Multifunctional Materials and Smart Systems (Energy Materials, Ferroelectric Materials, Metamaterials, Phononic Crystals)",
            "Advanced Manufacturing & Processing Techniques (Additive Manufacturing, Composite Manufacturing Methods)",
            "Multi-scale Modeling & Simulation (Molecular Dynamics, Novel Finite Element Methods, Phase-Field Method)",
            "Machine Learning in Computational Mechanics and Materials Sciences"
        ],
        "accommodation_dates": [
            "October 12, 2025 (Friday)",
            "October 13, 2025 (Saturday)", 
            "October 14, 2025 (Sunday)",
            "October 15, 2025 (Monday)",
            "October 16, 2025 (Tuesday)"
        ],
        "welcome_text": """...""",  # 你的欢迎文本
        "required_fields": ["paper_title", "authors_affiliations", "presenting_author", "corresponding_author", "session", "abstract", "contact_email"]
    },
    "zh": {
        "title": "智能材料力学研究生国际论坛",
        "subtitle": "中国上海 | 2025年10月13-15日",
        "paper_title": "论文标题",
        "author_name": "作者姓名",
        "author_affiliation": "所属单位",
        "add_author": "添加作者",
        "remove_author": "删除",
        "is_presenting": "报告人",
        "is_corresponding": "通讯作者",
        "authors_help": "添加所有作者的姓名、单位和角色信息",
        "session": "分会场主题",
        "abstract": "摘要",
        "abstract_help": "请提供详细的研究摘要或上传摘要文件",
        "abstract_upload": "上传摘要文件",
        "download_template": "下载模板",
        "accommodation": "住宿日期",
        "accommodation_help": "选择会议期间需要住宿的具体日期（仅限海外参会者）",
        "full_name": "姓名",
        "passport_number": "护照号",
        "accommodation_info": "住宿个人信息",
        "custom_dates": "其他日期（请注明）：",
        "dietary_requirements": "饮食要求",
        "dietary_help": "请说明饮食要求（会议期间餐饮安排）",
        "dietary_vegan": "纯素食",
        "dietary_vegetarian": "素食",
        "dietary_none": "无特殊要求", 
        "dietary_other": "其他（请注明）",
        "dietary_specify": "请具体说明您的饮食要求：",
        "contact_email": "联系邮箱",
        "contact_phone": "联系电话（可选）",
        "submit": "提交投稿",
        "reset": "重置表单",
        "success": "🎉 提交成功！我们将尽快与您联系。",
        "error": "❌ 请填写所有必填字段",
        "language": "语言",
        "my_submissions": "📋 我的投稿",
        "search_submissions": "🔍 查询我的投稿",
        "email_placeholder": "输入邮箱地址查看投稿记录",
        "search": "查询",
        "no_submissions": "该邮箱地址暂无投稿记录。",
        "admin_panel": "🛠️ 管理员面板",
        "admin_login": "管理员登录",
        "admin_password": "管理员密码",
        "login": "登录",
        "logout": "退出",
        "invalid_password": "❌ 密码错误",
        "file_uploaded": "✅ 文件上传成功",
        "file_error": "❌ 文件上传错误",
        "sessions": [
            "多功能材料与智能系统（能源材料、铁电材料、超材料、声子晶体）",
            "先进制造与加工技术（增材制造、复合材料制造方法）",
            "多尺度建模与仿真（分子动力学、新型有限元方法、相场方法）",
            "计算力学与材料科学中的机器学习"
        ],
        "accommodation_dates": [
            "2025年10月12日（周五）",
            "2025年10月13日（周六）",
            "2025年10月14日（周日）",
            "2025年10月15日（周一）",
            "2025年10月16日（周二）"
        ],
        "welcome_text": """...""",  # 你的欢迎文本
        "required_fields": ["paper_title", "authors_affiliations", "presenting_author", "corresponding_author", "session", "abstract", "contact_email"]
    }
}

# ============== 2. 然后是session state初始化 ==============
# 初始化会话状态
if 'language' not in st.session_state:
    st.session_state.language = 'en'
# ... 其他session state初始化

# ============== 3. 然后定义t函数 ==============
# 获取当前语言的文本 - 修复KeyError问题
def t(key):
    try:
        return LANGUAGES[st.session_state.language][key]
    except KeyError:
        # 如果键不存在，尝试使用英文版本
        try:
            return LANGUAGES['en'][key]
        except KeyError:
            # 如果英文版本也不存在，返回键本身
            return key

# ============== 4. 其他函数定义 ==============
# ... 你的其他函数 ...

# ============== 5. 侧边栏和主页面开始 ==============
# 侧边栏
with st.sidebar:
    # ... 侧边栏代码 ...

# 主页面
st.title(t("title"))
st.subheader(t("subtitle"))

# ============== 6. 在投稿表单部分，正确放置饮食需求代码 ==============
# 在这个位置找到：住宿日期部分代码
# 在住宿日期部分之后，住宿个人信息之前，添加：

# 饮食要求部分 - 正确位置
st.subheader(f"**{t('dietary_requirements')}:**")
st.markdown(t('dietary_help'))

dietary_options = [
    t('dietary_none'),
    t('dietary_vegetarian'), 
    t('dietary_vegan'),
    t('dietary_other')
]

dietary_requirement = st.radio(
    "Select your dietary requirement / 选择您的饮食要求:",
    dietary_options,
    index=0,
    key="dietary_radio"
)

dietary_other_text = ""
if dietary_requirement == t('dietary_other'):
    dietary_other_text = st.text_input(
        t('dietary_specify'),
        placeholder="e.g., Halal, Kosher, Gluten-free, Nut allergy, etc. / 例如：清真、犹太洁食、无麸质、坚果过敏等",
        key="dietary_other_input"
    )

# 然后继续住宿个人信息部分...

# ============== 7. 在form提交处理中添加饮食需求数据处理 ==============
# 在 if submitted: 部分中添加：
if submitted:
    # 获取饮食要求
    dietary_requirement = st.session_state.get('dietary_radio', t('dietary_none'))
    dietary_other_text = st.session_state.get('dietary_other_input', '')
    
    # 组合饮食要求信息
    final_dietary = dietary_requirement
    if dietary_requirement == t('dietary_other') and dietary_other_text.strip():
        final_dietary = f"{dietary_requirement}: {dietary_other_text.strip()}"
    
    # ... 其他验证代码 ...
    
    # 在submission字典中添加：
    submission = {
        # ... 其他字段 ...
        'dietary_requirements': final_dietary,  # 新增字段
        # ... 其他字段 ...
    }
