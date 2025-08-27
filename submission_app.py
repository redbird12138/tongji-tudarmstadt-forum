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
        "author_name": "Author Name",
        "author_affiliation": "Affiliation",
        "add_author": "Add Another Author",
        "remove_author": "Remove",
        "is_presenting": "Presenting Author",
        "is_corresponding": "Corresponding Author",
        "authors_help": "Add all authors with their affiliations and roles",
        "session": "Session",
        "abstract": "Abstract",
        "abstract_help": "Please provide a detailed abstract of your research",
        "accommodation": "Accommodation Dates",
        "accommodation_help": "Select specific nights you need accommodation during the conference period",
        "custom_dates": "Other dates (please specify):",
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
            "October 12, 2025 (Friday)",
            "October 13, 2025 (Saturday)", 
            "October 14, 2025 (Sunday)",
            "October 15, 2025 (Monday)",
            "October 16, 2025 (Tuesday)"
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
        "author_name": "作者姓名",
        "author_affiliation": "所属单位",
        "add_author": "添加作者",
        "remove_author": "删除",
        "is_presenting": "报告人",
        "is_corresponding": "通讯作者",
        "authors_help": "添加所有作者的姓名、单位和角色信息",
        "session": "分会场主题",
        "abstract": "摘要",
        "abstract_help": "请提供详细的研究摘要",
        "accommodation": "住宿日期",
        "accommodation_help": "选择会议期间需要住宿的具体日期",
        "custom_dates": "其他日期（请注明）：",
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
            "2025年10月12日（周五）",
            "2025年10月13日（周六）",
            "2025年10月14日（周日）",
            "2025年10月15日（周一）",
            "2025年10月16日（周二）"
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
if 'authors' not in st.session_state:
    st.session_state.authors = [{'name': '', 'affiliation': '', 'is_presenting': False, 'is_corresponding': False}]

# 数据文件路径
DATA_FILE = os.path.join(os.getcwd(), 'submissions.json')

# 安全获取字段值的辅助函数
def safe_get(submission, *keys):
    """安全获取提交数据中的字段值，支持多个备用键"""
    for key in keys:
        if key in submission and submission[key]:
            return submission[key]
    return "N/A"

# 格式化作者信息的辅助函数
def format_authors_display(submission):
    """格式化作者信息显示"""
    # 优先使用新格式的作者数据
    if 'authors_display' in submission:
        return submission['authors_display']
    
    # 如果有authors数组，格式化显示
    if 'authors' in submission and isinstance(submission['authors'], list):
        authors_text = []
        for author in submission['authors']:
            if isinstance(author, dict) and 'name' in author and 'affiliation' in author:
                roles = []
                if author.get('is_presenting'):
                    roles.append("Presenting")
                if author.get('is_corresponding'):
                    roles.append("Corresponding")
                
                role_text = f" ({', '.join(roles)})" if roles else ""
                authors_text.append(f"{author['name']} - {author['affiliation']}{role_text}")
        
        if authors_text:
            return "; ".join(authors_text)
    
    # 最后尝试使用旧格式
    return safe_get(submission, 'authors_affiliations', 'presenting_author')

# 获取报告作者信息
def get_presenting_authors(submission):
    """获取报告作者信息"""
    if 'presenting_authors' in submission and isinstance(submission['presenting_authors'], list):
        return "; ".join(submission['presenting_authors'])
    elif 'presenting_author' in submission:
        return submission['presenting_author']
    elif 'authors' in submission and isinstance(submission['authors'], list):
        presenting = [f"{a['name']} ({a['affiliation']})" for a in submission['authors'] if a.get('is_presenting')]
        return "; ".join(presenting) if presenting else "N/A"
    return "N/A"

# 获取通讯作者信息
def get_corresponding_authors(submission):
    """获取通讯作者信息"""
    if 'corresponding_authors' in submission and isinstance(submission['corresponding_authors'], list):
        return "; ".join(submission['corresponding_authors'])
    elif 'corresponding_author' in submission:
        return submission['corresponding_author']
    elif 'authors' in submission and isinstance(submission['authors'], list):
        corresponding = [f"{a['name']} ({a['affiliation']})" for a in submission['authors'] if a.get('is_corresponding')]
        return "; ".join(corresponding) if corresponding else "N/A"
    return "N/A"

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
    try:
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
                    unique_emails = len(set(s.get('contact_email', 'unknown') for s in submissions))
                    st.metric("👥 Unique Submitters", unique_emails)
                
                with col3:
                    accommodation_needed = len([s for s in submissions 
                                             if safe_get(s, 'accommodation_dates') != 'Not needed' and safe_get(s, 'accommodation_dates') != 'N/A'])
                    st.metric("🏨 Need Accommodation", accommodation_needed)
                
                with col4:
                    sessions = len(set(safe_get(s, 'session') for s in submissions if safe_get(s, 'session') != 'N/A'))
                    st.metric("📚 Active Sessions", sessions)
                
                # 最近提交
                st.subheader("🕒 Recent Submissions")
                recent_submissions = sorted(submissions, key=lambda x: x.get('submission_time', ''), reverse=True)[:5]
                
                for submission in recent_submissions:
                    with st.expander(f"📄 {safe_get(submission, 'paper_title')} - {safe_get(submission, 'submission_time')}"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write("**Authors:**", format_authors_display(submission))
                            st.write("**Session:**", safe_get(submission, 'session'))
                        with col2:
                            st.write("**Contact:**", safe_get(submission, 'contact_email'))
                            st.write("**Accommodation:**", safe_get(submission, 'accommodation_dates'))
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
                    unique_sessions = list(set(safe_get(s, 'session') for s in submissions if safe_get(s, 'session') != 'N/A'))
                    session_filter = st.selectbox("📚 Filter by Session", 
                                                options=["All Sessions"] + unique_sessions)
                
                # 应用过滤器
                filtered_submissions = submissions
                
                if search_term:
                    search_lower = search_term.lower()
                    filtered_submissions = [s for s in filtered_submissions 
                                          if (search_lower in safe_get(s, 'paper_title').lower() or
                                              search_lower in format_authors_display(s).lower() or
                                              search_lower in safe_get(s, 'contact_email').lower())]
                
                if session_filter != "All Sessions":
                    filtered_submissions = [s for s in filtered_submissions if safe_get(s, 'session') == session_filter]
                
                st.write(f"**Showing {len(filtered_submissions)} of {len(submissions)} submissions**")
                
                # 显示提交列表
                for i, submission in enumerate(filtered_submissions):
                    with st.expander(f"📄 [{safe_get(submission, 'submission_id')}] {safe_get(submission, 'paper_title')}"):
                        col1, col2 = st.columns([2, 1])
                        
                        with col1:
                            st.write("**Title:**", safe_get(submission, 'paper_title'))
                            st.write("**Authors:**", format_authors_display(submission))
                            st.write("**Presenting Authors:**", get_presenting_authors(submission))
                            st.write("**Corresponding Authors:**", get_corresponding_authors(submission))
                            st.write("**Session:**", safe_get(submission, 'session'))
                            st.write("**Abstract:**")
                            st.text_area("", safe_get(submission, 'abstract'), height=100, disabled=True, key=f"abstract_{i}")
                        
                        with col2:
                            st.write("**Contact Info:**")
                            st.write("📧", safe_get(submission, 'contact_email'))
                            contact_phone = safe_get(submission, 'contact_phone')
                            if contact_phone != 'N/A':
                                st.write("📱", contact_phone)
                            
                            st.write("**Details:**")
                            st.write("🆔", safe_get(submission, 'submission_id'))
                            st.write("⏰", safe_get(submission, 'submission_time'))
                            st.write("🌐", safe_get(submission, 'language'))
                            st.write("🏨", safe_get(submission, 'accommodation_dates'))
                            
                            # 删除按钮
                            st.markdown("---")
                            delete_key = f"delete_{i}_{safe_get(submission, 'submission_id')}"
                            confirm_key = f"confirm_delete_{i}_{safe_get(submission, 'submission_id')}"
                            
                            if st.button(f"🗑️ Delete", key=delete_key, type="secondary"):
                                if st.session_state.get(confirm_key, False):
                                    # 执行删除
                                    all_submissions = load_data()
                                    submission_id = safe_get(submission, 'submission_id')
                                    updated_submissions = [s for s in all_submissions if safe_get(s, 'submission_id') != submission_id]
                                    save_data(updated_submissions)
                                    st.success("Submission deleted successfully!")
                                    # 清除确认状态
                                    if confirm_key in st.session_state:
                                        del st.session_state[confirm_key]
                                    st.rerun()
                                else:
                                    # 第一次点击，要求确认
                                    st.session_state[confirm_key] = True
                                    st.warning("Click again to confirm deletion. This action cannot be undone!")
                                    st.rerun()
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
                    session = safe_get(submission, 'session')
                    if session != 'N/A':
                        session_counts[session] = session_counts.get(session, 0) + 1
                
                if session_counts:
                    session_df = pd.DataFrame(list(session_counts.items()), columns=['Session', 'Count'])
                    st.bar_chart(session_df.set_index('Session'))
                else:
                    st.info("No session data available for visualization.")
                
                # 住宿需求
                st.write("**🏨 Accommodation Analysis:**")
                accommodation_needed = len([s for s in submissions 
                                         if safe_get(s, 'accommodation_dates') not in ['Not needed', 'N/A', '']])
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
                try:
                    # 为导出准备数据
                    export_data = []
                    for s in submissions:
                        export_record = {
                            'Submission_ID': safe_get(s, 'submission_id'),
                            'Paper_Title': safe_get(s, 'paper_title'),
                            'Authors': format_authors_display(s),
                            'Presenting_Authors': get_presenting_authors(s),
                            'Corresponding_Authors': get_corresponding_authors(s),
                            'Session': safe_get(s, 'session'),
                            'Abstract': safe_get(s, 'abstract'),
                            'Contact_Email': safe_get(s, 'contact_email'),
                            'Contact_Phone': safe_get(s, 'contact_phone'),
                            'Accommodation_Dates': safe_get(s, 'accommodation_dates'),
                            'Submission_Time': safe_get(s, 'submission_time'),
                            'Language': safe_get(s, 'language')
                        }
                        export_data.append(export_record)
                    
                    df = pd.DataFrame(export_data)
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
                                'Submission_ID': safe_get(s, 'submission_id'),
                                'Title': safe_get(s, 'paper_title'),
                                'Presenting_Author': get_presenting_authors(s),
                                'Email': safe_get(s, 'contact_email'),
                                'Session': safe_get(s, 'session'),
                                'Accommodation': safe_get(s, 'accommodation_dates'),
                                'Submission_Time': safe_get(s, 'submission_time')
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
                    
                    # 显示数据预览
                    st.subheader("📋 Data Preview")
                    st.dataframe(df.head(10), use_container_width=True)
                    
                except Exception as e:
                    st.error(f"Export error: {str(e)}")
                    st.info("Please check the data format and try again.")
            else:
                st.info("No data to export.")
                
    except Exception as e:
        st.error(f"Admin Dashboard Error: {str(e)}")
        st.info("Please refresh the page or contact the administrator.")

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
                user_submissions = [s for s in submissions if safe_get(s, 'contact_email').lower() == search_email.lower()]
                
                if user_submissions:
                    st.success(f"Found {len(user_submissions)} submission(s) for {search_email}")
                    
                    for submission in user_submissions:
                        with st.expander(f"📄 {safe_get(submission, 'paper_title')} (Submitted: {safe_get(submission, 'submission_time')})"):
                            col1, col2 = st.columns([2, 1])
                            
                            with col1:
                                st.write("**Title:**", safe_get(submission, 'paper_title'))
                                st.write("**Authors:**", format_authors_display(submission))
                                st.write("**Presenting Authors:**", get_presenting_authors(submission))
                                st.write("**Corresponding Authors:**", get_corresponding_authors(submission))
                                st.write("**Session:**", safe_get(submission, 'session'))
                                st.write("**Contact:**", safe_get(submission, 'contact_email'))
                                contact_phone = safe_get(submission, 'contact_phone')
                                if contact_phone != 'N/A':
                                    st.write("**Phone:**", contact_phone)
                                st.write("**Accommodation:**", safe_get(submission, 'accommodation_dates'))
                            
                            with col2:
                                st.write("**Submission ID:**", safe_get(submission, 'submission_id'))
                                st.write("**Language:**", safe_get(submission, 'language'))
                                st.write("**Status:**", "✅ Submitted")
                            
                            st.write("**Abstract:**")
                            st.write(safe_get(submission, 'abstract'))
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

        # Authors management (outside form)
        st.subheader(f"**{t('authors_help')} *:**")
        
        # Display existing authors
        for i, author in enumerate(st.session_state.authors):
            with st.container():
                st.write(f"**Author {i+1}:**")
                col_name, col_affiliation = st.columns(2)
                
                with col_name:
                    author['name'] = st.text_input(
                        t('author_name'),
                        value=author['name'],
                        key=f"author_name_{i}",
                        placeholder="John Smith"
                    )
                
                with col_affiliation:
                    author['affiliation'] = st.text_input(
                        t('author_affiliation'),
                        value=author['affiliation'],
                        key=f"author_affiliation_{i}",
                        placeholder="Tongji University"
                    )
                
                col_present, col_corresp, col_remove = st.columns([1, 1, 1])
                with col_present:
                    author['is_presenting'] = st.checkbox(
                        t('is_presenting'),
                        value=author['is_presenting'],
                        key=f"is_presenting_{i}"
                    )
                
                with col_corresp:
                    author['is_corresponding'] = st.checkbox(
                        t('is_corresponding'),
                        value=author['is_corresponding'],
                        key=f"is_corresponding_{i}"
                    )
                
                with col_remove:
                    if len(st.session_state.authors) > 1:
                        if st.button(t('remove_author'), key=f"remove_{i}"):
                            st.session_state.authors.pop(i)
                            st.rerun()
                
                st.markdown("---")
        
        # Add new author button (outside form)
        if st.button(t('add_author')):
            st.session_state.authors.append({
                'name': '', 
                'affiliation': '', 
                'is_presenting': False, 
                'is_corresponding': False
            })
            st.rerun()

        with st.form("submission_form", clear_on_submit=False):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                paper_title = st.text_input(
                    f"{t('paper_title')} *",
                    placeholder="Enter your paper title here..."
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
                
                # Custom dates option
                custom_dates = st.text_input(
                    t('custom_dates'),
                    placeholder="e.g., October 11, October 17, etc."
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
                # Validate authors
                valid_authors = [a for a in st.session_state.authors if a['name'].strip() and a['affiliation'].strip()]
                presenting_authors = [a for a in valid_authors if a['is_presenting']]
                corresponding_authors = [a for a in valid_authors if a['is_corresponding']]
                
                # Format authors for display
                authors_text = []
                for i, author in enumerate(valid_authors):
                    roles = []
                    if author['is_presenting']:
                        roles.append("Presenting")
                    if author['is_corresponding']:
                        roles.append("Corresponding")
                    
                    role_text = f" ({', '.join(roles)})" if roles else ""
                    authors_text.append(f"{author['name']} - {author['affiliation']}{role_text}")
                
                authors_display = "; ".join(authors_text)
                
                # Combine accommodation dates
                all_accommodation = []
                if accommodation_dates:
                    all_accommodation.extend(accommodation_dates)
                if custom_dates.strip():
                    all_accommodation.append(f"Custom: {custom_dates.strip()}")
                
                accommodation_display = "; ".join(all_accommodation) if all_accommodation else "Not needed"
                
                # Validation
                missing_fields = []
                if not paper_title.strip():
                    missing_fields.append("Paper Title")
                if not valid_authors:
                    missing_fields.append("At least one author with name and affiliation")
                if not presenting_authors:
                    missing_fields.append("At least one presenting author")
                if not corresponding_authors:
                    missing_fields.append("At least one corresponding author")
                if not session:
                    missing_fields.append("Session")
                if not abstract.strip():
                    missing_fields.append("Abstract")
                if not contact_email.strip():
                    missing_fields.append("Contact Email")
                
                if not missing_fields:
                    submission_id = generate_submission_id(contact_email, paper_title)
                    
                    submission = {
                        'submission_id': submission_id,
                        'paper_title': paper_title,
                        'authors': valid_authors,
                        'authors_display': authors_display,
                        'presenting_authors': [f"{a['name']} ({a['affiliation']})" for a in presenting_authors],
                        'corresponding_authors': [f"{a['name']} ({a['affiliation']})" for a in corresponding_authors],
                        'session': session,
                        'abstract': abstract,
                        'contact_email': contact_email,
                        'contact_phone': contact_phone,
                        'accommodation_dates': accommodation_display,
                        'submission_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'language': st.session_state.language
                    }
                    
                    submissions = load_data()
                    submissions.append(submission)
                    save_data(submissions)
                    
                    # Reset authors for next submission
                    st.session_state.authors = [{'name': '', 'affiliation': '', 'is_presenting': False, 'is_corresponding': False}]
                    
                    st.success(t('success'))
                    st.balloons()
                    
                    with st.expander("📋 Submission Summary"):
                        st.write("**Submission ID:**", submission_id)
                        st.write("**Title:**", paper_title)
                        st.write("**Authors:**", authors_display)
                        st.write("**Presenting Authors:**", "; ".join(submission['presenting_authors']))
                        st.write("**Corresponding Authors:**", "; ".join(submission['corresponding_authors']))
                        st.write("**Session:**", session)
                        st.write("**Contact:**", contact_email)
                        if all_accommodation:
                            st.write("**Accommodation:**", accommodation_display)
                        st.write("**Submission Time:**", submission['submission_time'])
                        
                        st.info("💡 **Tip:** Save your Submission ID for future reference!")
                    
                else:
                    st.error(t('error'))
                    st.write("Missing required fields:")
                    for field in missing_fields:
                        st.write(f"- {field}")


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
