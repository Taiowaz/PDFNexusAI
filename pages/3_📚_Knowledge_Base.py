import datetime
import os
import streamlit as st
from SQLite_Manager import sqlite
from Pinecone_Manager import api_pinecone
from PDF_Processor import pdf_processor


st.set_page_config(
    page_icon="📚",
    page_title="Knowledge Base"
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


# 知识库名输入框禁用状态
st.session_state.disabled_text_input = False
# 知识库名称输入框参数
st.session_state.label_text_input_kbs = "Create A New Knowledge Base"
st.session_state.placeholder_text_input_kbs = "Enter a Knowledge Base Name"
# text_input_kbs的key变量,用于重复渲染
st.session_state.key_text_input_kbs = 0
# 删除按钮的key变量,用于重复渲染
st.session_state.key_button_delete = 0

# 更新知识库下拉框数据函数


def update_selectbox_kbs():
    st.session_state.disabled_selectbox_kbs = False
    # 更新知识库下拉框数据
    st.session_state.knowledgebases = sqlite.get_all_vectorbase_name_db()
    return selectbox_kbs_placeholder.selectbox(
        label=st.session_state.label_text_input_kbs,
        options=st.session_state.knowledgebases,
        placeholder=st.session_state.placeholder_text_input_kbs,
        index=None,
        disabled=st.session_state.disabled_selectbox_kbs
    )
# 更新知识库文本输入框


def update_text_input_kbs():
    st.session_state.key_text_input_kbs += 1
    text_input_kbs = text_input_kbs_placeholder.text_input(
        label=st.session_state.label_text_input_kbs,
        placeholder=st.session_state.placeholder_text_input_kbs,
        # value=st.session_state.selected_kb, # 选中已有知识库时，不会显示当前值，故注释
        key="text_input"+str(st.session_state.key_text_input_kbs),
        disabled=st.session_state.disabled_text_input
    )
    return text_input_kbs

# 更新删除按钮状态


def update_button_delete():
    st.session_state.key_button_delete += 1
    return button_delete_placeholder.button(
        type="primary",
        label="Delete",
        use_container_width=True,
        key="button_delete"+str(st.session_state.key_button_delete),
        disabled=not st.session_state.disabled_text_input  # 创建新知识库时,删除按钮禁用
    )


# 删除库并更新知识库名称


def delete_upddate_kb():
    # 删除知识库
    print(st.session_state.selected_kb)
    sqlite.delete_vector_base_info(st.session_state.selected_kb)
    api_pinecone.delete_vectorbase(st.session_state.selected_kb)

    # 更新相关参数
    st.session_state.disabled_text_input = False
    st.session_state.label_text_input_kbs = "Create A New Knowledge Base"
    st.session_state.placeholder_text_input_kbs = "Enter a Knowledge Base Name"
    st.session_state.selected_kb = None
    # 更新知识库下拉框
    update_selectbox_kbs()
    # 更新知识库名称输入框
    update_text_input_kbs()
    # 更新删除按钮状态
    update_button_delete()
    st.toast("Knowledge Base deleted successfully!", icon="🎉")

# 添加并更新知识库


def add_update_kb():
    # 读取上传的PDF文件，并保存在临时文件夹中
    def read_pdf(upload_pdfs) -> str:
        # 创建临时文件夹
        pdf_folder = "file/temp/" + \
            str(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
        os.makedirs(pdf_folder, exist_ok=True)  # 忽略已存在的文件夹导致的异常
        # 保存PDF文件
        for pdf in upload_pdfs:
            # 构建保存路径
            pdf_name = pdf.name
            dest = os.path.join(pdf_folder, pdf_name)
            # 保存文件
            with open(dest, "wb") as f:
                f.write(pdf.read())
        return pdf_folder

    if selectbox_kbs:
        # 已存在知识库上传pdf
        # 上传文件不为空
        if upload_pdfs:
            st.session_state.disabled_selectbox_kbs = True
            # 读取上传的PDF文件
            pdf_folder = read_pdf(upload_pdfs)
            # 向已有知识库中添加PDF报告
            pdf_processor.process_pdf_vectorbase_in_threads(
                selectbox_kbs, pdf_folder)
            st.session_state.disabled_selectbox_kbs = False
            st.toast("PDF report processed successfully!", icon="🎉")
    else:
        # 创建新知识库
        if text_input_kbs:
            # 创建新知识库，并可以添加PDF报告
            if not sqlite.vector_base_exists(text_input_kbs):
                # 知识库名不冲突
                sqlite.create_vectorbase_info(text_input_kbs)
                api_pinecone.create_vectorbase(text_input_kbs)
                # 上传文件不为空
                if upload_pdfs:
                    st.session_state.disabled_selectbox_kbs = True
                    # 读取上传的PDF文件
                    pdf_folder = read_pdf(upload_pdfs)
                    # 向已有知识库中添加PDF报告
                    sqlite.process_pdf_vectorbase_in_threads(
                        selectbox_kbs, pdf_folder)
                    st.session_state.disabled_selectbox_kbs = False
                    # 更新文件上传组件
                st.toast(
                    "Knowledge Base created and PDF report processed successfully!",
                    icon="🎉")
                # 更新知识库下拉框
                update_selectbox_kbs()
                # 更新知识库名称输入框
                st.session_state.disabled_text_input = False
                st.session_state.label_text_input_kbs = "Create A New Knowledge Base"
                st.session_state.placeholder_text_input_kbs = "Enter a Knowledge Base Name"
                st.session_state.selected_kb = None
                update_text_input_kbs()
                # 更新删除按钮状态
                update_button_delete()
            else:
                # 知识库名冲突
                st.toast("Knowledge Base name already exists.", icon="⚠️")
        else:
            # 提示输入有效知识库名称
            st.toast("Please enter a valid knowledge base name.", icon="⚠️")


st.title("📚Knowledge Base")
st.markdown("---")

# 知识库下拉框
with st.sidebar:
    # 先占位，后续更新知识库下拉框数据
    selectbox_kbs_placeholder = st.empty()
    # 更新知识库下拉框数据
    selectbox_kbs = update_selectbox_kbs()

    # 设置会话参数,用于控制知识库名称输入框
    # 选中已有知识库，禁用编辑名字,同时将选中值以placeholder参数显示在输入框中
    if selectbox_kbs:
        st.session_state.selected_kb = selectbox_kbs
        st.session_state.disabled_text_input = True
        st.session_state.label_text_input_kbs = "Current Knowledge Base Name"
        st.session_state.placeholder_text_input_kbs = selectbox_kbs
    else:
        # 未选用知识库，创建新知识库,可编辑名字
        st.session_state.selected_kb = selectbox_kbs
        st.session_state.disabled_text_input = False
        st.session_state.label_text_input_kbs = "Create A New Knowledge Base"
        st.session_state.placeholder_text_input_kbs = "Enter a Knowledge Base Name"

text_input_kbs_placeholder = st.empty()
# 更新知识库名称输入框
text_input_kbs = update_text_input_kbs()

# 上传PDF文件组件

upload_pdfs = st.file_uploader(
    label="Upload PDF Report",
    type=["pdf"],
    accept_multiple_files=True
)
# 按钮组件
col1, col2 = st.columns(2)
with col1:
    button_delete_placeholder = st.empty()
    button_delete = update_button_delete()
    if button_delete:
        selectbox_kbs = delete_upddate_kb()
with col2:
    button_save = st.button(
        label="Save",
        use_container_width=True,
        type="secondary",
    )
    if button_save:
        selectbox_kbs = add_update_kb()
