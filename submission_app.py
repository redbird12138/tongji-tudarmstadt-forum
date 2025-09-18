# Add these entries to the LANGUAGES dictionary

# In the "en" section, add these new entries:
"dietary_requirements": "Dietary Requirements",
"dietary_help": "Please specify any dietary requirements (for catering during the conference)",
"dietary_vegan": "Vegan",
"dietary_vegetarian": "Vegetarian", 
"dietary_none": "No special requirements",
"dietary_other": "Other (please specify)",
"dietary_specify": "Please specify your dietary requirements:",

# In the "zh" section, add these new entries:
"dietary_requirements": "饮食要求",
"dietary_help": "请说明饮食要求（会议期间餐饮安排）",
"dietary_vegan": "纯素食",
"dietary_vegetarian": "素食",
"dietary_none": "无特殊要求", 
"dietary_other": "其他（请注明）",
"dietary_specify": "请具体说明您的饮食要求：",

# Here's the complete updated section where you need to add the dietary requirements:

# Replace the accommodation section in your main form area with this updated version:

# 住宿日期部分 - 在表单外处理
st.subheader(f"**{t('accommodation')}:**")
st.markdown(t('accommodation_help'))

# 创建复选框网格
accommodation_cols = st.columns(3)
selected_dates = []

for i, date_option in enumerate(t('accommodation_dates')):
    col_index = i % 3
    with accommodation_cols[col_index]:
        if st.checkbox(date_option, key=f"accom_date_outside_{i}"):
            selected_dates.append(date_option)

# 其他日期选项
other_dates_needed = st.checkbox("Other dates / 其他日期")
custom_dates = ""
if other_dates_needed:
    custom_dates = st.text_input(
        t('custom_dates'),
        placeholder="e.g., October 11, October 17, etc.",
        key="custom_dates"
    )

# 饮食要求部分 - 新增
st.subheader(f"**{t('dietary_requirements')}:**")
st.markdown(t('dietary_help'))

dietary_options = [
    t('dietary_none'),
    t('dietary_vegetarian'), 
    t('dietary_vegan'),
    t('dietary_other')
]

dietary_requirement = st.radio(
    "Select your dietary requirement:",
    dietary_options,
    index=0,
    key="dietary_radio"
)

dietary_other_text = ""
if dietary_requirement == t('dietary_other'):
    dietary_other_text = st.text_input(
        t('dietary_specify'),
        placeholder="e.g., Halal, Kosher, Gluten-free, Nut allergy, etc.",
        key="dietary_other_input"
    )

# 住宿个人信息 - 在表单外处理
accommodation_needed = bool(selected_dates or custom_dates.strip())
full_name = ""
passport_number = ""

if accommodation_needed:
    st.subheader(f"**{t('accommodation_info')} *:**")
    col1, col2 = st.columns(2)
    
    with col1:
        full_name = st.text_input(
            f"{t('full_name')} *",
            placeholder="John Smith",
            help="Required for accommodation booking",
            key="full_name_outside"
        )
    
    with col2:
        passport_number = st.text_input(
            f"{t('passport_number')} *",
            placeholder="A12345678", 
            help="Required for accommodation booking",
            key="passport_outside"
        )

# In the form submission validation section, add dietary requirements to the submission data:

if submitted:
    # 获取表单外的数据
    full_name = st.session_state.get('full_name_outside', '')
    passport_number = st.session_state.get('passport_outside', '')
    
    # 获取饮食要求
    dietary_requirement = st.session_state.get('dietary_radio', t('dietary_none'))
    dietary_other_text = st.session_state.get('dietary_other_input', '')
    
    # 组合饮食要求信息
    final_dietary = dietary_requirement
    if dietary_requirement == t('dietary_other') and dietary_other_text.strip():
        final_dietary = f"{dietary_requirement}: {dietary_other_text.strip()}"
    
    # ... existing validation code ...
    
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
            'dietary_requirements': final_dietary,  # NEW FIELD
            'full_name': full_name if accommodation_needed else 'N/A',
            'passport_number': passport_number if accommodation_needed else 'N/A',
            'submission_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'language': st.session_state.language
        }
        
        # ... rest of submission code ...

# Update the admin dashboard display sections to include dietary requirements:

# In the admin_dashboard function, update the display sections:

# For the overview section, add dietary info to the expander:
with st.expander(f"📄 {safe_get(submission, 'paper_title')} - {safe_get(submission, 'submission_time')}"):
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Authors:**", format_authors_display(submission))
        st.write("**Session:**", safe_get(submission, 'session'))
    with col2:
        st.write("**Contact:**", safe_get(submission, 'contact_email'))
        st.write("**Accommodation:**", safe_get(submission, 'accommodation_dates'))
        st.write("**Dietary:**", safe_get(submission, 'dietary_requirements'))  # NEW

# For the detailed submissions view, add to the right column:
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
    st.write("🍽️", safe_get(submission, 'dietary_requirements'))  # NEW
    
    # ... rest of the display code ...

# Update the export section to include dietary requirements:

# In the admin export section, update the export_record:
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
    'Dietary_Requirements': safe_get(s, 'dietary_requirements'),  # NEW
    'Submission_Time': safe_get(s, 'submission_time'),
    'Language': safe_get(s, 'language')
}

# Update the user submissions view to show dietary requirements:

# In the my_submissions section:
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
        st.write("**Dietary Requirements:**", safe_get(submission, 'dietary_requirements'))  # NEW
    
    # ... rest of the display code ...

# Update the submission summary display:
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
    st.write("**Dietary Requirements / 饮食要求:**", final_dietary)  # NEW
    if uploaded_file_name:
        st.write("**Uploaded File / 上传文件:**", uploaded_file_name)
    st.write("**Submission Time / 提交时间:**", submission['submission_time'])
    
    st.info("💡 **Tip:** Save your Submission ID for future reference! / 请保存您的提交编号以备查询！")
