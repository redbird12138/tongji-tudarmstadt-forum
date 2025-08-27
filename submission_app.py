import streamlit as st
import pandas as pd
from datetime import datetime
import json
import os
import hashlib

# 页面配置
st.set_page_config(
    page_title="International Forum System",
    page_icon="🎓",
    layout="wide"
)

# 管理员密码
ADMIN_PASSWORD = "tongji2025"

# 语言配置
LANGUAGES = {
    "en": {
        "title": "International Forum of Graduate Students on Mechanics of Smart Materials",
        "subtitle": "Shanghai, China | October 13-15, 2025",
        "paper_title": "Paper Title",
        "authors_affiliations": "Authors & Affiliations",
        "authors_help": "Please provide all authors' names and their affiliations",
        "presenting_author": "Presenting Author",
        "presenting_author_help": "The person who will give the presentation at the conference",
        "corresponding_author": "Corresponding Author",
        "corresponding_author_help": "The main contact person for this submission",
        "session": "Session",
        "abstract": "Abstract",
        "abstract_help": "Please provide a detailed abstract of your research",
        "accommodation": "Accommodation Dates",
        "accommodation_help": "Select which nights you need accommodation during Oct 12-16, 2025",
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
        "sessions": [
            "Multifunctional Materials (Energy Storage, Ferroelectric Materials, Metamaterials)",
            "Advanced Manufacturing & Processing Techniques (Additive Manufacturing, 3D Printing, Novel Fabrication)",
            "Multi-scale Modeling & Simulation (Molecular Dynamics, Finite Element, Phase-field Methods)",
            "Machine Learning in Computational Mechanics & Materials Science (AI-driven Design, Data-driven Methods)"
        ],
        "dates": [
            "Oct 12 (4 nights: 12-16)",
            "Oct 13 (3 nights: 13-16)", 
            "Oct 14 (2 nights: 14-16)",
            "Oct 15 (1 night: 15-16)"
        ],
        "welcome_text": """
        **Welcome to the International Forum of Graduate Students on Mechanics of Smart Materials!**
        
        This forum is jointly organized by **Tongji University** and **TU Darmstadt (Technische Universität Darmstadt)** to strengthen academic collaboration in the field of smart materials mechanics.
        
        We welcome submissions on **TOPICS** including but not limited to:
        - **Composite Materials & Structural Mechanics**
        - **Energy Materials & Storage Systems** 
        - **Functional Materials & Smart Systems**
        - **Soft Electronics & Bio-inspired Robotics**
        - **Metamaterials & Phononic Crystals**
        - **Aircraft & Aerospace Materials**
        
        **Research Approaches Welcome:**
        - Theoretical and experimental contributions
        - Multi-scale modeling and simulation
        - Data-driven and Machine Learning methods
        - Computational mechanics approaches
        
        **Registration & Fees:**
        - No registration fee required
        - Oral presentation participants: **free accommodations** available Oct 12-16 (4 nights)
        - Travel expenses covered by participants
        
        **Contact:** 19531@tongji.edu.cn (Prof. Zhao) | **Organizers:** Tongji University & TU Darmstadt
        """,
        "required_fields": ["paper_title", "authors_affiliations", "presenting_author", "corresponding_author", "session", "abstract", "contact_email"]
    },
    "zh": {
        "title": "智能材料力学研究生国际论坛",
        "subtitle": "中国上海 | 2025年10月13-15日",
        "paper_title": "论文标题",
        "authors_affiliations": "作者姓名及单位",
        "authors_help": "请提供所有作者姓名及其所在单位",
        "presenting_author": "报告人",
        "presenting_author_help": "在会议上进行报告的人员",
        "corresponding_author": "通讯作者",
        "corresponding_author_help": "本次投稿的主要联系人",
        "session": "分会场主题",
        "abstract": "摘要",
        "abstract_help": "请提供详细的研究摘要",
        "accommodation": "住宿日期",
        "accommodation_help": "请选择2025年10月12-16日期间需要住宿的日期",
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
        "sessions": [
            "多功能材料（储能材料、铁电材料、超材料）",
            "先进制造与加工技术（增材制造、3D打印、新型制备工艺）",
            "多尺度建模与仿真（分子动力学、有限元、相场方法）",
            "机器学习在计算力学与材料科学中的应用（AI驱动设计、数据驱动方法）"
        ],
        "dates": [
            "10月12日（4晚：12-16日）",
            "10月13日（3晚：13-16日）",
            "10月14日（2晚：14-16日）",
            "10月15日（1晚：15-16日）"
        ],
        "welcome_text": """
        **欢迎参加智能材料力学研究生国际论坛！**
        
        本论坛由**同济大学**与**达姆施塔特工业大学(TU Darmstadt)**联合主办，旨在加强智能材料力学领域的学术合作。
        
        欢迎关于以下**主题**的投稿：
        - **复合材料与结构力学**
        - **能源材料与储能系统**
        - **功能材料与智能系统**
        - **软体电子学与仿生机器人学**
        - **超材料与声子晶体**
        - **航空航天材料**
        
        **欢迎的研究方法：**
        - 理论和实验研究
        - 多尺度建模与仿真
        - 数据驱动与机器学习方法
        - 计算力学方法
        
        **注册与费用：**
        - 无需注册费
        - 口头报告参与者：可申请**免费住宿**（10月12-16日，4晚）
        - 差旅费用需自行承担
        
        **联系方式：** 19531@tongji.edu.cn（赵教授）| **主办方：** 同济大学 & 达姆施塔特工业大学
        """,
        "required_fields": ["paper_title", "authors_affiliations", "presenting_author", "corresponding_author", "session", "abstract", "contact_email"]
    }
}

# 初始化会话状态
if 'language' not in st.session_state:
    st.session_state.language = 'en'
if 'current_view' not in st.session_state:
    st.session_state.current_view = 'submit'
if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False

# 数据文件路径
DATA_FILE = os.path.join(os.getcwd(), 'submissions.json')

# 加载已保存的数据
def load_data():
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data
        else:
            return []
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return []

# 保存数据
def save_data(submissions):
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(submissions, f, ensure_ascii=False, indent=2)
    except Exception as e:
        st.error(f"Error saving data: {e}")

# 生成提交ID
def generate_submission_id(email, title):
    content = f"{email.lower()}{title.lower()}{datetime.now().strftime('%Y%m%d')}"
    return hashlib.md5(content.encode()).hexdigest()[:8]

# 获取当前语言的文本
def t(key):
    return LANGUAGES[st.session_state.language][key]

# 管理员登录界面
def admin_login():
    st.header("🔐 " + t("admin_login"))
    
    with st.form("admin_login_form"):
        password = st.text_input(t("admin_password"), type="password")
        login_button = st.form_submit_button(t("login"), type="primary")
        
        if login_button:
            if password == ADMIN_PASSWORD:
                st.session_state.is_admin = True
                st.session_state.current_view = 'admin_overview'
                st.success("✅ Login successful!")
                st.rerun()
            else:
                st.error(t("invalid_password"))

# 管理员界面
def admin_dashboard():
    submissions = load_data()
    
    st.header("🛠️ Admin Dashboard")
    st.markdown("**Conference Management System**")
    
    # 顶部导航
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("📊 Overview", use_container_width=True):
            st.session_state.current_view = 'admin_overview'
            st.rerun()
    
    with col2:
        if st.button("📋 All Submissions", use_container_width=True):
            st.session_state.current_view = 'admin_submissions'
            st.rerun()
    
    with col3:
        if st.button("📈 Analytics", use_container_width=True):
            st.session_state.current_view = 'admin_analytics'
            st.rerun()
    
    with col4:
        if st.button("⚙️ Export Data", use_container_width=True):
            st.session_state.current_view = 'admin_export'
            st.rerun()
    
    with col5:
        if st.button(t("logout"), use_container_width=True):
            st.session_state.is_admin = False
            st.session_state.current_view = 'submit'
            st.rerun()
    
    st.markdown("---")
    
    # 管理员概览
    if st.session_state.current_view == 'admin_overview':
        st.subheader("📊 Conference Overview")
        
        if submissions:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("📝 Total Submissions", len(submissions))
            
            with col2:
                unique_emails = len(set(s['contact_email'] for s in submissions))
                st.metric("👥 Unique Submitters", unique_emails)
            
            with col3:
                accommodation_needed = len([s for s in submissions if s.get('accommodation_dates', 'Not needed') != 'Not needed'])
                st.metric("🏨 Need Accommodation", accommodation_needed)
            
            with col4:
                sessions = len(set(s['session'] for s in submissions))
                st.metric("📚 Active Sessions", sessions)
            
            # 最近提交
            st.subheader("🕒 Recent Submissions")
            recent_submissions = sorted(submissions, key=lambda x: x['submission_time'], reverse=True)[:5]
            
            for submission in recent_submissions:
                with st.expander(f"📄 {submission['paper_title']} - {submission['submission_time']}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write("**Authors:**", submission['authors_affiliations'])
                        st.write("**Session:**", submission['session'])
                    with col2:
                        st.write("**Contact:**", submission['contact_email'])
                        st.write("**Accommodation:**", submission['accommodation_dates'])
        else:
            st.info("No submissions yet.")
    
    # 所有投稿管理
    elif st.session_state.current_view == 'admin_submissions':
        st.subheader("📋 All Submissions Management")
        
        if submissions:
            # 搜索和过滤
            col1, col2 = st.columns(2)
            
            with col1:
                search_term = st.text_input("🔍 Search", placeholder="Search by title, author, or email")
            
            with col2:
                session_filter = st.selectbox("📚 Filter by Session", 
                                            options=["All Sessions"] + list(set(s['session'] for s in submissions)))
            
            # 应用过滤器
            filtered_submissions = submissions
            
            if search_term:
                filtered_submissions = [s for s in filtered_submissions 
                                      if search_term.lower() in s['paper_title'].lower() 
                                      or search_term.lower() in s['authors_affiliations'].lower()
                                      or search_term.lower() in s['contact_email'].lower()]
            
            if session_filter != "All Sessions":
                filtered_submissions = [s for s in filtered_submissions if s['session'] == session_filter]
            
            st.write(f"**Showing {len(filtered_submissions)} of {len(submissions)} submissions**")
            
            # 显示提交列表
            for i, submission in enumerate(filtered_submissions):
                with st.expander(f"📄 [{submission.get('submission_id', 'N/A')}] {submission['paper_title']}"):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.write("**Title:**", submission['paper_title'])
                        st.write("**Authors:**", submission['authors_affiliations'])
                        st.write("**Presenting Author:**", submission['presenting_author'])
                        st.write("**Corresponding Author:**", submission['corresponding_author'])
                        st.write("**Session:**", submission['session'])
                        st.write("**Abstract:**")
                        st.text_area("", submission['abstract'], height=100, disabled=True, key=f"abstract_{i}")
                    
                    with col2:
                        st.write("**Contact Info:**")
                        st.write("📧", submission['contact_email'])
                        if submission.get('contact_phone'):
                            st.write("📱", submission['contact_phone'])
                        
                        st.write("**Details:**")
                        st.write("🆔", submission.get('submission_id', 'N/A'))
                        st.write("⏰", submission['submission_time'])
                        st.write("🌐", submission['language'])
                        st.write("🏨", submission['accommodation_dates'])
        else:
            st.info("No submissions available.")
    
    # 分析页面
    elif st.session_state.current_view == 'admin_analytics':
        st.subheader("📈 Conference Analytics")
        
        if submissions:
            # 按会话分布
            st.write("**📊 Submissions by Session:**")
            session_counts = {}
            for submission in submissions:
                session = submission['session']
                session_counts[session] = session_counts.get(session, 0) + 1
            
            session_df = pd.DataFrame(list(session_counts.items()), columns=['Session', 'Count'])
            st.bar_chart(session_df.set_index('Session'))
            
            # 住宿需求
            st.write("**🏨 Accommodation Analysis:**")
            accommodation_needed = len([s for s in submissions 
                                     if s.get('accommodation_dates', 'Not needed') != 'Not needed'])
            accommodation_not_needed = len(submissions) - accommodation_needed
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Need Accommodation", accommodation_needed)
            with col2:
                st.metric("No Accommodation Needed", accommodation_not_needed)
                
        else:
            st.info("No data available for analysis.")
    
    # 数据导出
    elif st.session_state.current_view == 'admin_export':
        st.subheader("📊 Export Data")
        
        if submissions:
            # 完整数据导出
            df = pd.DataFrame(submissions)
            csv_data = df.to_csv(index=False, encoding='utf-8')
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.download_button(
                    label="📊 Export All Data (CSV)",
                    data=csv_data,
                    file_name=f'all_submissions_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
                    mime='text/csv',
                    use_container_width=True
                )
            
            with col2:
                # 简化版导出
                summary_data = []
                for s in submissions:
                    summary_data.append({
                        'Submission_ID': s.get('submission_id', 'N/A'),
                        'Title': s['paper_title'],
                        'Presenting_Author': s['presenting_author'],
                        'Email': s['contact_email'],
                        'Session': s['session'],
                        'Accommodation': s['accommodation_dates'],
                        'Submission_Time': s['submission_time']
                    })
                
                summary_df = pd.DataFrame(summary_data)
                summary_csv = summary_df.to_csv(index=False, encoding='utf-8')
                st.download_button(
                    label="📋 Export Summary (CSV)",
                    data=summary_csv,
                    file_name=f'submission_summary_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
                    mime='text/csv',
                    use_container_width=True
                )
            
            st.info(f"📈 Total Submissions Available: {len(submissions)}")
        else:
            st.info("No data to export.")

# 侧边栏
with st.sidebar:
    st.header("⚙️ Settings")
    
    # 语言切换
    new_language = st.selectbox(
        t("language"),
        options=['en', 'zh'],
        format_func=lambda x: "English" if x == 'en' else "中文",
        index=0 if st.session_state.language == 'en' else 1
    )
    
    if new_language != st.session_state.language:
        st.session_state.language = new_language
        st.rerun()
    
    st.divider()
    
    # 导航菜单
    st.header("📋 Navigation")
    
    if not st.session_state.is_admin:
        if st.button("📝 New Submission", use_container_width=True):
            st.session_state.current_view = 'submit'
            st.rerun()
        
        if st.button(t("my_submissions"), use_container_width=True):
            st.session_state.current_view = 'my_submissions'
            st.rerun()
        
        if st.button(t("admin_panel"), use_container_width=True):
            st.session_state.current_view = 'admin_login'
            st.rerun()
    else:
        st.success("👤 Admin Mode Active")
        if st.button("👥 User Mode", use_container_width=True):
            st.session_state.is_admin = False
            st.session_state.current_view = 'submit'
            st.rerun()

# 主页面
st.title(t("title"))
st.subheader(t("subtitle"))

# 管理员登录
if st.session_state.current_view == 'admin_login' and not st.session_state.is_admin:
    admin_login()

# 管理员界面
elif st.session_state.is_admin and st.session_state.current_view.startswith('admin'):
    admin_dashboard()

# 用户界面
else:
    # 会议信息
    if st.session_state.current_view == 'submit':
        with st.expander("ℹ️ Conference Information / 会议信息", expanded=True):
            st.markdown(t("welcome_text"))

    # 查看我的投稿
    if st.session_state.current_view == 'my_submissions':
        st.header(t("my_submissions"))
        
        search_email = st.text_input(
            t("search_submissions"),
            placeholder=t("email_placeholder"),
            key="search_email"
        )
        
        if st.button(t("search")):
            if search_email:
                submissions = load_data()
                user_submissions = [s for s in submissions if s['contact_email'].lower() == search_email.lower()]
                
                if user_submissions:
                    st.success(f"Found {len(user_submissions)} submission(s) for {search_email}")
                    
                    for submission in user_submissions:
                        with st.expander(f"📄 {submission['paper_title']} (Submitted: {submission['submission_time']})"):
                            col1, col2 = st.columns([2, 1])
                            
                            with col1:
                                st.write("**Title:**", submission['paper_title'])
                                st.write("**Authors:**", submission['authors_affiliations'])
                                st.write("**Presenting Author:**", submission['presenting_author'])
                                st.write("**Corresponding Author:**", submission['corresponding_author'])
                                st.write("**Session:**", submission['session'])
                                st.write("**Contact:**", submission['contact_email'])
                                if submission.get('contact_phone'):
                                    st.write("**Phone:**", submission['contact_phone'])
                                st.write("**Accommodation:**", submission['accommodation_dates'])
                            
                            with col2:
                                st.write("**Submission ID:**", submission.get('submission_id', 'N/A'))
                                st.write("**Language:**", submission['language'])
                                st.write("**Status:**", "✅ Submitted")
                            
                            st.write("**Abstract:**")
                            st.write(submission['abstract'])
                else:
                    st.info(t("no_submissions"))
            else:
                st.warning("Please enter an email address")
        
        if st.button("🔙 Back to Submission Form"):
            st.session_state.current_view = 'submit'
            st.rerun()

    # 投稿表单
    if st.session_state.current_view == 'submit':
        st.header("📝 Submission Form / 投稿表单")

        with st.form("submission_form", clear_on_submit=True):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                paper_title = st.text_input(
                    f"{t('paper_title')} *",
                    placeholder="Enter your paper title here..."
                )
                
                authors_affiliations = st.text_area(
                    f"{t('authors_affiliations')} *",
                    height=100,
                    help=t('authors_help'),
                    placeholder="Example:\nJohn Smith¹, Jane Doe², Michael Chen¹\n¹Tongji University, Shanghai, China\n²TU Darmstadt, Germany"
                )
                
                presenting_author = st.text_input(
                    f"{t('presenting_author')} *",
                    help=t('presenting_author_help'),
                    placeholder="John Smith (Tongji University)"
                )
                
                corresponding_author = st.text_input(
                    f"{t('corresponding_author')} *", 
                    help=t('corresponding_author_help'),
                    placeholder="Jane Doe (jane.doe@tu-darmstadt.de)"
                )
                
                session = st.selectbox(
                    f"{t('session')} *",
                    options=t('sessions'),
                    index=0
                )
            
            with col2:
                contact_email = st.text_input(
                    f"{t('contact_email')} *",
                    placeholder="your.email@university.edu"
                )
                
                contact_phone = st.text_input(
                    t('contact_phone'),
                    placeholder="+86 138xxxx"
                )
                
                accommodation_dates = st.multiselect(
                    t('accommodation'),
                    options=t('dates'),
                    help=t('accommodation_help')
                )
            
            abstract = st.text_area(
                f"{t('abstract')} *",
                height=200,
                help=t('abstract_help'),
                placeholder="Please provide a detailed abstract of your research (200-500 words recommended)..."
            )
            
            col1, col2, col3 = st.columns([1, 1, 1])
            
            with col2:
                submitted = st.form_submit_button(t('submit'), type="primary", use_container_width=True)
            
            with col3:
                reset = st.form_submit_button(t('reset'), use_container_width=True)
            
            if submitted:
                required_data = {
                    'paper_title': paper_title,
                    'authors_affiliations': authors_affiliations,
                    'presenting_author': presenting_author,
                    'corresponding_author': corresponding_author,
                    'session': session,
                    'abstract': abstract,
                    'contact_email': contact_email
                }
                
                if all(required_data.values()):
                    submission_id = generate_submission_id(contact_email, paper_title)
                    
                    submission = {
                        'submission_id': submission_id,
                        'paper_title': paper_title,
                        'authors_affiliations': authors_affiliations,
                        'presenting_author': presenting_author,
                        'corresponding_author': corresponding_author,
                        'session': session,
                        'abstract': abstract,
                        'contact_email': contact_email,
                        'contact_phone': contact_phone,
                        'accommodation_dates': ', '.join(accommodation_dates) if accommodation_dates else 'Not needed',
                        'submission_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'language': st.session_state.language
                    }
                    
                    submissions = load_data()
                    submissions.append(submission)
                    save_data(submissions)
                    
                    st.success(t('success'))
                    st.balloons()
                    
                    with st.expander("📋 Submission Summary"):
                        st.write("**Submission ID:**", submission_id)
                        st.write("**Title:**", paper_title)
                        st.write("**Authors:**", authors_affiliations)
                        st.write("**Presenting Author:**", presenting_author)
                        st.write("**Corresponding Author:**", corresponding_author)
                        st.write("**Session:**", session)
                        st.write("**Contact:**", contact_email)
                        if accommodation_dates:
                            st.write("**Accommodation:**", ', '.join(accommodation_dates))
                        st.write("**Submission Time:**", submission['submission_time'])
                        
                        st.info("💡 **Tip:** Save your Submission ID for future reference!")
                    
                else:
                    st.error(t('error'))
                    missing_fields = [field for field, value in required_data.items() if not value]
                    st.write("Missing fields:", missing_fields)

# 页脚
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
        <p>School of Aerospace Engineering and Applied Mechanics, Tongji University<br>
        同济大学航空航天与力学学院<br>
        <strong>In Collaboration with TU Darmstadt (Technische Universität Darmstadt)</strong><br>
        <strong>与达姆施塔特工业大学合作举办</strong></p>
        <p>For technical support, contact: peng05@tongji.edu.cn</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# CSS样式
st.markdown("""
<style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    
    .stForm {
        background-color: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        border: 1px solid #e9ecef;
    }
    
    .metric-container {
        background-color: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)
