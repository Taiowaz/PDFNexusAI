import streamlit as st
from SQLite_Manager import sqlite

st.set_page_config(
    page_icon="🍻",
    page_title="Chat Session"
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


st.session_state.key_text_input_cs_name = 0
st.session_state.key_button_delete = 0
st.session_state.key_selectbox_cs = 0
# 更新下拉框


def update_selectbox_cs():
    st.session_state.key_selectbox_cs += 1
    st.session_state.chat_session_names = sqlite.get_all_chat_session_name()
    selectbox_cs = selectbox_cs_placeholder.selectbox(
        label="Choose Chat Session",
        options=st.session_state.chat_session_names,
        key="selectbox_cs"+str(st.session_state.key_selectbox_cs),
    )
    # 记录当前下拉框选中的值
    st.session_state.current_selected_cs_name = selectbox_cs
    if selectbox_cs == None:
        st.session_state.disabled_flag_chat_session = True
    return selectbox_cs
# 更新文本输入框


def update_text_input_cs_name():
    st.session_state.key_text_input_cs_name += 1
    return text_input_cs_name_placeholder.text_input(
        label="Modify Chat Session Name",
        placeholder="Enter a Chat Session Name",
        value=st.session_state.current_selected_cs_name,
        key="text_input_cs_name"+str(st.session_state.key_text_input_cs_name),
        disabled=st.session_state.disabled_flag_chat_session
    )
# 更新删除按钮


def update_button_delete():
    st.session_state.key_button_delete += 1
    # 删除最后一个会话时，不能禁用，需重新渲染
    return button_delete_placeholder.button(
        type="primary",
        label="Delete",
        key="button_delete"+str(st.session_state.key_button_delete),
        use_container_width=True,
        disabled=st.session_state.disabled_flag_chat_session
    )


st.title("🍻Chat Session")
st.markdown("---")

with st.sidebar:
    selectbox_cs_placeholder = st.empty()
    selectbox_cs = update_selectbox_cs()
    st.session_state.current_selected_cs_name = selectbox_cs

    if st.session_state.current_selected_cs_name == None:
        st.session_state.disabled_flag_chat_session = True
    else:
        st.session_state.disabled_flag_chat_session = False


text_input_cs_name_placeholder = st.empty()
text_input_cs_name = update_text_input_cs_name()
col1, col2, col3 = st.columns(3)
with col1:
    button_delete_placeholder = st.empty()
    button_delete = update_button_delete()
    if button_delete:
        # 删除chatbot当前会话,清空messages，current_chat_cs_name
        if 'current_chat_cs_name' in st.session_state and st.session_state.current_selected_cs_name == st.session_state.current_chat_cs_name:
            st.session_state.messages = []
            st.session_state.current_chat_cs_name = None
        sqlite.delete_chat_session(
            st.session_state.current_selected_cs_name)
        st.toast("Chat Session deleted successfully!", icon="🎉")
        # 更新下拉框
        update_selectbox_cs()
        # 更新输入框
        update_text_input_cs_name()
        # 更新删除按钮
        update_button_delete()
with col2:
    button_save = st.button(
        label="Save",
        use_container_width=True,
        type="secondary",
        disabled=st.session_state.disabled_flag_chat_session,
    )
    # 更新会话名
    if button_save:
        if sqlite.chat_session_exists(text_input_cs_name):
            # 会话名已存在
            st.toast("Chat Session Name already exists!", icon="⚠️")
        else:
            sqlite.update_chat_session_name(
                name=st.session_state.current_selected_cs_name,
                new_name=text_input_cs_name
            )
            st.toast("Chat Session Name updated successfully!", icon="🎉")
            old_cs_name = st.session_state.current_selected_cs_name
            new_cs_name = text_input_cs_name
            # 更新下拉框
            update_selectbox_cs()
            # 更新输入框
            update_text_input_cs_name()
            # 若当chat有会话，且正是修改的会话，则更新当前会话名
            if ("current_chat_cs_name" in st.session_state
                    and st.session_state.current_chat_cs_name == old_cs_name):
                st.session_state.current_chat_cs_name = new_cs_name

with col3:
    button_load = st.button(
        label="Load",
        use_container_width=True,
        type="secondary",
        disabled=st.session_state.disabled_flag_chat_session,
    )
    if button_load:
        # current_chat_cs_name 为chat所在会话名
        # current_selected_cs_name 为当前下拉框选中的会话名
        st.session_state.current_chat_cs_name = st.session_state.current_selected_cs_name
        st.session_state.messages = sqlite.get_messages_by_chat_session_name(
            st.session_state.current_chat_cs_name)
        st.switch_page("pages/1_🤖_Chat_Bot.py")
