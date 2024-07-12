import streamlit as st



# 设置网页窗口标题
st.set_page_config(
    page_title="PDFNexusAI - Welcome",
    page_icon="👋"
)

# 设置网页左上角LOGO
st.markdown(
    """
        <style>
            [data-testid="stSidebarNav"] {
                background-image: url("https://img2.imgtp.com/2024/05/02/SKfvNhPU.png");
                background-repeat: no-repeat;
                background-size: contain;
                padding-top: 30px;
                background-position: 0px 20px;
            }
        </style>
        """,
    unsafe_allow_html=True,
)



st.write("# 🎉Welcome to PDFNexusAI!👋")


st.markdown(
    """
    PDFNexusAI is my graduation project. \n
    This application can disassemble your PDF reports and increase the professional capabilities of LLM.
    """
)

st.markdown("---")

st.markdown("#### Talk with ChatBot🤖")
st.page_link(
    page="pages/1_🤖_Chat_Bot.py",
    label="# ChatBot",
    icon="🤖",
)

st.markdown("#### Manage Chat Session🍻")
st.page_link(
    page="pages/2_🍻_Chat_Session.py",
    label="# Chat Session",
    icon="🍻",
)

st.markdown("#### Create Knowledge Base📚")
st.page_link(
    page="pages/3_📚_Knowledge_Base.py",
    label="# Knowledge Base",
    icon="📚",
)

st.markdown(
    """
    ---
    """
)

st.markdown("#### About Me 👨‍💻")
st.markdown(
    """
    - Name:         Debin Han \n
    - University:   Beijing Science and Technology Information University \n
    - Major:        Information management and information system\n
    - Phone number: 188-1077-3656 \n
    - Email:        taiowa@foxmail.com\n
    """
)
