from SQLite_Manager import sqlite
from dashscope import Generation
from dashscope.api_entities.dashscope_response import Role
from http import HTTPStatus
import random

# 普通回复
# 用于判定是否需要查询知识库
# 以及对知识库进行描述


def call_qwen(messages: list) -> str:
    resp = Generation.call(
        model=Generation.Models.qwen_plus,
        messages=messages,
        # 设置返回结果为message格式
        result_format='message',
    )

    if resp.status_code == HTTPStatus.OK:
        return resp.output.choices[0]['message']['content']
    else:
        print("\nError: ", resp)


# 流式输出回复


def call_stream_with_messages(chat_session_name, messages: list):
    # 生成器函数
    def stream():
        resps = Generation.call(
            model=Generation.Models.qwen_plus,
            messages=messages,
            result_format='message',
            stream=True,
            temperature=0.01,       # 设置输出随意度
            incremental_output=True,     # 增量式流式输出
        )
        content = ""
        for resp in resps:
            if resp.status_code == HTTPStatus.OK:
                content_incre = resp.output.choices[0]['message']['content']
                content += content_incre
                yield content_incre
        # 存储到数据库中
        sqlite.save_message_by_chat_session_name(
            chat_session_name=chat_session_name,
            message={
                'role': 'assistant',
                'content': content
            }
        )
    # 返回生成器
    return stream()
