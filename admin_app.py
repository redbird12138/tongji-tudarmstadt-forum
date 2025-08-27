import streamlit as st
import pandas as pd
from datetime import datetime
import json
import os
import hashlib

# 页面配置
st.set_page_config(
    page_title="Conference Admin Dashboard",
    page_icon="🛠️",
    layout="wide"
)

# 管理员密码配置（在实际使用中应该使用更安全的方式）
ADMIN_PASSWORD = "tongji2025"  # 请修改为更安全的密码

# 初始化会话状态
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'current_view' not in st.session_state:
    st.session_state.current_view = 'overview'

# 数据文件路径
DATA_FILE = os.path.join(os.getcwd(), 'submissions.json')

# 加载数据
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

# 验证管理员身份
def authenticate():
    st.title("🔐 Admin Login")
    st.markdown("---")
    
    with st.form("login_form"):
        st.write("**International Forum Admin Dashboard**")
        password = st.text_input("Enter Admin Password", type="password")
        login_button = st.form_submit_button("Login", type="primary")
        
        if login_button:
            if password == ADMIN_PASSWORD:
                st.session_state.authenticated = True
                st.success("✅ Login successful!")
                st.rerun()
            else:
                st.error("❌ Invalid password. Please try again.")

# 管理员仪表板
def admin_dashboard():
    submissions = load_data()
    
    # 顶部菜单
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        if st.button("📊 Overview", use_container_width=True):
            st.session_state.current_view = 'overview'
            st.rerun()
    
    with col2:
        if st.button("📋 All Submissions", use_container_width=True):
            st.session_state.current_view = 'submissions'
            st.rerun()
    
    with col3:
        if st.button("📈 Analytics", use_container_width=True):
            st.session_state.current_view = 'analytics'
            st.rerun()
    
    with col4:
        if st.button("⚙️ Settings", use_container_width=True):
            st.session_state.current_view = 'settings'
            st.rerun()
    
    with col5:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()
    
    st.markdown("---")
    
    # 概览页面
    if st.session_state.current_view == 'overview':
        st.header("📊 Conference Overview")
        
        # 统计卡片
        if submissions:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    label="📝 Total Submissions",
                    value=len(submissions),
                    delta=f"+{len([s for s in submissions if s['submission_time'].startswith(datetime.now().strftime('%Y-%m-%d'))])}"
                )
            
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
            st.info("No submissions yet. The conference dashboard will show statistics once submissions start coming in.")
    
    # 所有投稿页面
    elif st.session_state.current_view == 'submissions':
        st.header("📋 All Submissions Management")
        
        if submissions:
            # 搜索和过滤
            col1, col2, col3 = st.columns(3)
            
            with col1:
                search_term = st.text_input("🔍 Search", placeholder="Search by title, author, or email")
            
            with col2:
                session_filter = st.selectbox("📚 Filter by Session", 
                                            options=["All Sessions"] + list(set(s['session'] for s in submissions)))
            
            with col3:
                accommodation_filter = st.selectbox("🏨 Accommodation Filter", 
                                                  ["All", "Needed", "Not Needed"])
            
            # 应用过滤器
            filtered_submissions = submissions
            
            if search_term:
                filtered_submissions = [s for s in filtered_submissions 
                                      if search_term.lower() in s['paper_title'].lower() 
                                      or search_term.lower() in s['authors_affiliations'].lower()
                                      or search_term.lower() in s['contact_email'].lower()]
            
            if session_filter != "All Sessions":
                filtered_submissions = [s for s in filtered_submissions if s['session'] == session_filter]
            
            if accommodation_filter == "Needed":
                filtered_submissions = [s for s in filtered_submissions 
                                      if s.get('accommodation_dates', 'Not needed') != 'Not needed']
            elif accommodation_filter == "Not Needed":
                filtered_submissions = [s for s in filtered_submissions 
                                      if s.get('accommodation_dates', 'Not needed') == 'Not needed']
            
            st.write(f"**Showing {len(filtered_submissions)} of {len(submissions)} submissions**")
            
            # 导出功能
            if st.button("📥 Export Filtered Results to CSV"):
                df = pd.DataFrame(filtered_submissions)
                csv = df.to_csv(index=False, encoding='utf-8')
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name=f'submissions_filtered_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
                    mime='text/csv'
                )
            
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
                        
                        st.write("**Submission Details:**")
                        st.write("🆔", submission.get('submission_id', 'N/A'))
                        st.write("⏰", submission['submission_time'])
                        st.write("🌐", submission['language'])
                        st.write("🏨", submission['accommodation_dates'])
                        
                        # 删除按钮（危险操作）
                        if st.button(f"🗑️ Delete", key=f"delete_{i}", type="secondary"):
                            submissions.remove(submission)
                            save_data(submissions)
                            st.success("Submission deleted!")
                            st.rerun()
        else:
            st.info("No submissions available.")
    
    # 分析页面
    elif st.session_state.current_view == 'analytics':
        st.header("📈 Conference Analytics")
        
        if submissions:
            # 按会话分布
            st.subheader("📊 Submissions by Session")
            session_counts = {}
            for submission in submissions:
                session = submission['session']
                session_counts[session] = session_counts.get(session, 0) + 1
            
            # 创建会话统计图表
            session_df = pd.DataFrame(list(session_counts.items()), columns=['Session', 'Count'])
            st.bar_chart(session_df.set_index('Session'))
            
            # 时间分布
            st.subheader("📅 Submissions Over Time")
            submission_dates = [datetime.strptime(s['submission_time'].split()[0], '%Y-%m-%d').date() 
                              for s in submissions]
            
            date_counts = {}
            for date in submission_dates:
                date_counts[date] = date_counts.get(date, 0) + 1
            
            date_df = pd.DataFrame(list(date_counts.items()), columns=['Date', 'Submissions'])
            st.line_chart(date_df.set_index('Date'))
            
            # 语言分布
            st.subheader("🌐 Language Distribution")
            language_counts = {}
            for submission in submissions:
                lang = submission.get('language', 'Unknown')
                language_counts[lang] = language_counts.get(lang, 0) + 1
            
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Language Statistics:**")
                for lang, count in language_counts.items():
                    st.write(f"- {lang.upper()}: {count}")
            
            # 住宿需求
            st.subheader("🏨 Accommodation Analysis")
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
    
    # 设置页面
    elif st.session_state.current_view == 'settings':
        st.header("⚙️ System Settings")
        
        st.subheader("🗂️ Data Management")
        
        # 数据备份
        if st.button("💾 Create Data Backup"):
            if submissions:
                backup_data = {
                    'backup_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'submission_count': len(submissions),
                    'submissions': submissions
                }
                
                backup_json = json.dumps(backup_data, ensure_ascii=False, indent=2)
                st.download_button(
                    label="📥 Download Backup File",
                    data=backup_json,
                    file_name=f'forum_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json',
                    mime='application/json'
                )
            else:
                st.info("No data to backup.")
        
        st.subheader("📊 Export Options")
        
        # 完整数据导出
        if submissions:
            # Excel导出
            df = pd.DataFrame(submissions)
            
            col1, col2 = st.columns(2)
            with col1:
                csv_data = df.to_csv(index=False, encoding='utf-8')
                st.download_button(
                    label="📊 Export All Data (CSV)",
                    data=csv_data,
                    file_name=f'all_submissions_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
                    mime='text/csv',
                    use_container_width=True
                )
            
            with col2:
                # 简化版导出（只包含关键信息）
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
        
        st.subheader("🔒 Security")
        st.info("Current admin password is active. Consider changing it periodically for security.")
        
        st.subheader("ℹ️ System Information")
        st.write(f"**Total Submissions:** {len(submissions)}")
        st.write(f"**Data File:** submissions.json")
        st.write(f"**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# 主程序
if not st.session_state.authenticated:
    authenticate()
else:
    st.title("🛠️ Conference Admin Dashboard")
    st.markdown("**International Forum of Graduate Students on Mechanics of Smart Materials**")
    admin_dashboard()

# CSS样式
st.markdown("""
<style>
    .stApp {
        max-width: 1400px;
        margin: 0 auto;
    }
    
    .metric-container {
        background-color: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
    }
    
    .stButton > button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)
