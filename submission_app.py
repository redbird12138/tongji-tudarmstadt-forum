# 1. 首先用上面的完整LANGUAGES字典替换你现有的LANGUAGES字典

# 2. 在住宿日期部分之后添加饮食需求部分：

# 饮食要求部分 - 新增在住宿日期之后
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

# 3. 在表单提交处理部分，修改如下：

if submitted:
    # 获取表单外的数据
    full_name = st.session_state.get('full_name_outside', '')
    passport_number = st.session_state.get('passport_outside', '')
    
    # 获取选择的住宿日期
    selected_dates = []
    for i, date_option in enumerate(t('accommodation_dates')):
        if st.session_state.get(f"accom_date_outside_{i}", False):
            selected_dates.append(date_option)
    
    # 获取其他日期
    custom_dates = st.session_state.get("custom_dates", "")
    
    # 获取饮食要求
    dietary_requirement = st.session_state.get('dietary_radio', t('dietary_none'))
    dietary_other_text = st.session_state.get('dietary_other_input', '')
    
    # 组合饮食要求信息
    final_dietary = dietary_requirement
    if dietary_requirement == t('dietary_other') and dietary_other_text.strip():
        final_dietary = f"{dietary_requirement}: {dietary_other_text.strip()}"
    
    # 验证作者
    valid_authors = [a for a in st.session_state.authors if a['name'].strip() and a['affiliation'].strip()]
    presenting_authors = [a for a in valid_authors if a['is_presenting']]
    corresponding_authors = [a for a in valid_authors if a['is_corresponding']]
    
    # 格式化作者显示
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
    
    # 合并住宿日期
    all_accommodation = []
    if selected_dates:
        all_accommodation.extend(selected_dates)
    if custom_dates.strip():
        all_accommodation.append(f"Custom: {custom_dates.strip()}")
    
    accommodation_display = "; ".join(all_accommodation) if all_accommodation else "Not needed"
    
    # 摘要处理 - 优先使用上传的文件
    final_abstract = uploaded_abstract_content if uploaded_abstract_content else abstract
    
    # 验证必填字段
    missing_fields = []
    if not paper_title.strip():
        missing_fields.append("Paper Title / 论文标题")
    if not valid_authors:
        missing_fields.append("At least one author with name and affiliation / 至少一位作者的姓名和单位")
    if not presenting_authors:
        missing_fields.append("At least one presenting author / 至少一位报告作者")
    if not corresponding_authors:
        missing_fields.append("At least one corresponding author / 至少一位通讯作者")
    if not session:
        missing_fields.append("Session / 分会场主题")
    if not final_abstract.strip():
        missing_fields.append("Abstract (either text or uploaded file) / 摘要（文本或上传文件）")
    if not contact_email.strip():
        missing_fields.append("Contact Email / 联系邮箱")
    
    # 住宿相关验证
    accommodation_needed = bool(selected_dates or custom_dates.strip())
    if accommodation_needed:
        if not full_name.strip():
            missing_fields.append("Full Name (required for accommodation) / 姓名（住宿必填）")
        if not passport_number.strip():
            missing_fields.append("Passport Number (required for accommodation) / 护照号（住宿必填）")
    
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
            'abstract': final_abstract,
            'abstract_file_name': uploaded_file_name if uploaded_file_name else 'N/A',
            'contact_email': contact_email,
            'contact_phone': contact_phone if contact_phone else 'N/A',
            'accommodation_dates': accommodation_display,
            'dietary_requirements': final_dietary,  # 新增字段
            'full_name': full_name if accommodation_needed else 'N/A',
            'passport_number': passport_number if accommodation_needed else 'N/A',
            'submission_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'language': st.session_state.language
        }
        
        submissions = load_data()
        submissions.append(submission)
        save_data(submissions)
        
        # 重置作者和上传文件
        st.session_state.authors = [{'name': '', 'affiliation': '', 'is_presenting': False, 'is_corresponding': False}]
        st.session_state.uploaded_abstract = None
        
        st.success(t('success'))
        st.balloons()
        
        with st.expander("📋 Submission Summary / 提交摘要"):
            st.write("**Submission ID / 提交编号:**", submission_id)
            st.write("**Title / 标题:**", paper_title)
            st.write("**Authors / 作者:**", authors_display)
            st.write("**Presenting Authors / 报告作者:**", "; ".join(submission['presenting_authors']))
            st.write("**Corresponding Authors / 通讯作者:**", "; ".join(submission['corresponding_authors']))
            st.write("**Session / 分会场:**", session)
            st.write("**Contact / 联系方式:**", contact_email)
            if all_accommodation:
                st.write("**Accommodation / 住宿:**", accommodation_display)
                if accommodation_needed:
                    st.write("**Full Name / 姓名:**", full_name)
                    st.write("**Passport Number / 护照号:**", passport_number)
            st.write("**Dietary Requirements / 饮食要求:**", final_dietary)  # 新增显示
            if uploaded_file_name:
                st.write("**Uploaded File / 上传文件:**", uploaded_file_name)
            st.write("**Submission Time / 提交时间:**", submission['submission_time'])
            
            st.info("💡 **Tip:** Save your Submission ID for future reference! / 请保存您的提交编号以备查询！")
    
    else:
        st.error(t('error'))
        st.write("Missing required fields / 缺少必填字段:")
        for field in missing_fields:
            st.write(f"- {field}")

# 4. 在管理员面板显示部分，添加饮食要求显示：

# 在admin_dashboard函数的详细提交查看部分，右列添加：
st.write("**Details:**")
st.write("🆔", safe_get(submission, 'submission_id'))
st.write("⏰", safe_get(submission, 'submission_time'))
st.write("🌐", safe_get(submission, 'language'))
st.write("🏨", safe_get(submission, 'accommodation_dates'))
st.write("🍽️", safe_get(submission, 'dietary_requirements'))  # 新增

# 5. 在用户查看投稿部分，添加饮食要求显示：

# 在my_submissions部分添加：
st.write("**Accommodation:**", safe_get(submission, 'accommodation_dates'))
st.write("**Dietary Requirements / 饮食要求:**", safe_get(submission, 'dietary_requirements'))  # 新增

# 6. 在数据导出部分，添加饮食要求字段：

# 在admin_dashboard的export部分，export_record字典中添加：
export_record = {
    'Submission_ID': safe_get(s, 'submission_id'),
    'Paper_Title': safe_get(s, 'paper_title'),
    'Authors': format_authors_display(s),
    'Presenting_Authors': get_presenting_authors(s),
    'Corresponding_Authors': get_corresponding_authors(s),
    'Session': safe_get(s, 'session'),
    'Abstract': safe_get(s, 'abstract'),
    'Abstract_File': safe_get(s, 'abstract_file_name'),
    'Contact_Email': safe_get(s, 'contact_email'),
    'Contact_Phone': safe_get(s, 'contact_phone'),
    'Full_Name': safe_get(s, 'full_name'),
    'Passport_Number': safe_get(s, 'passport_number'),
    'Accommodation_Dates': safe_get(s, 'accommodation_dates'),
    'Dietary_Requirements': safe_get(s, 'dietary_requirements'),  # 新增
    'Submission_Time': safe_get(s, 'submission_time'),
    'Language': safe_get(s, 'language')
}
