from SQLite_Manager import sqlite
from LLM.api import api_qwen
from LLM import prompt_createor
import sys
sys.path.append("/root/history/PDFNexusAI-LangChain")


# 与千问对话 --保存对话时，不带提示词，输入到模型的是带提示词的内容


def talk_stream_with_qwen(chat_session_name, vectorbase_name, messages: list):
    input_content = messages[-1]['content']
    # 保存当前消息,但不带提示词存入数据库
    sqlite.save_message_by_chat_session_name(
        chat_session_name=chat_session_name,
        message=messages[-1]
    )

    # 选定知识库，则根据知识库构建内容
    if vectorbase_name != None:
        # 意图识别
        flag = is_query_with_qwen(messages, vectorbase_name)
        print(f"\nflag:{flag}\n")
        if flag.lower().strip('.') == "yes":
            input_content = prompt_createor.create_prompt_for_input(
                content=input_content,
                vectorbase_name=vectorbase_name
            )
    """ 测试 """
    print(f"\ninput_content:{input_content}\n")
    # 构建messages 输入到LLM的内容，带有提示词
    messages[-1]['content'] = input_content
    print(f"\nmessages:{messages}\n")

    # 向qwenAPI发送请求并流式输出
    stream_gen = api_qwen.call_stream_with_messages(
        chat_session_name, messages)

    # 返回流响应流
    return stream_gen


def is_query_with_qwen(messages: list, vectorbase_name: str):
    # 获取用户输入
    current_input = messages[-1]['content']
    # 构建提示内容
    prompt = prompt_createor.create_prompt_is_query(
        current_input=current_input,
        vectorbase_name=vectorbase_name
    )
    print(f"\nprompt:{prompt}\n")
    # 构建messages 输入到LLM的内容，带有提示词
    messages[-1]['content'] = prompt
    # 向qwenAPI
    return api_qwen.call_qwen(messages)
