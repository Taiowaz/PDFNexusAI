import time
import streamlit as st
from SQLite_Manager import sqlite
from LLM import chat

st.set_page_config(
    page_icon="🤖",
    page_title="Chat Bot"
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


# 初始化加载数据
if "messages" not in st.session_state:
    st.session_state.messages = []
if "knowledgebases" not in st.session_state:
    st.session_state.knowledgebases = sqlite.get_all_vectorbase_name_db()
if "current_chat_cs_name" not in st.session_state:
    st.session_state.current_chat_cs_name = None


st.title("🤖ChatBot")
st.divider()

# 知识库下拉框
with st.sidebar:
    button_clear_chat = st.button(
        label="New Chat",
        type="primary",
        use_container_width=True,
    )
    # 清空对话
    if button_clear_chat:
        st.session_state.messages = []
        st.session_state.current_chat_cs_name = None
    st.markdown("---")
    selected_kb = st.selectbox(
        label="Choose Current Knowledge Base",
        options=st.session_state.knowledgebases,
        index=None,
    )


# Display chat messages from history on app rerun
for message in st.session_state.messages:
    if message["role"] == "user":
        name = "user"
        avatar = "file/avatar/user.jpg"
    else:
        name = "ai"
        avatar = "file/avatar/ai.png"
    with st.chat_message(name=name, avatar=avatar):
        st.markdown(message["content"])

# React to user input
# := 代表content赋值并判None
if content := st.chat_input("Type a message..."):
    # Display user message in chat message container
    with st.chat_message(name="user", avatar="file/avatar/user.jpg"):
        st.markdown(content)
    # 用户输入消息后，判断当前会话是否存在,不存在则自动创建
    if st.session_state.current_chat_cs_name == None:
        st.session_state.current_chat_cs_name = sqlite.save_chat_session_return_name()
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": content})

    # !!!函数 qwen对话流式回复
    def ai_resp_gen():
        messages = st.session_state.messages
        knowledgebase_name = selected_kb
        ai_resp_stream = chat.talk_stream_with_qwen(
            chat_session_name=st.session_state.current_chat_cs_name,
            vectorbase_name=knowledgebase_name,
            messages=messages
        )

        for resp_incre in ai_resp_stream:
            # 千问API流式输出是以多个字符增量返回的，为便于用户阅读，按字符流式输出
            for char in resp_incre:
                yield char
                time.sleep(0.05)

    # Display assistant response in chat message container
    with st.chat_message(name="ai", avatar="file/avatar/ai.png"):
        resp = st.write_stream(ai_resp_gen())
        # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": resp})
