from .models import VectorBaseInfo, ChatSession, Message
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine

# 创建一个SQLite数据库引擎
engine = create_engine('sqlite:///pdf_nexus_ai.db',
                       echo=False, logging_name=None)  # 日志开关

# 使用 scoped_session 创建一个有范围的会话工厂
Session = scoped_session(sessionmaker(bind=engine))

""" VectorBase操作 """

# 创建向量库信息


def create_vectorbase_info(vector_base_name):
    session = Session()
    vector_base_info = VectorBaseInfo(name=vector_base_name)
    session.add(vector_base_info)
    session.commit()
    session.close()


# 获取所有VectorBase


def get_all_vectorbase_name_db():
    session = Session()
    vectorbase_infos = session.query(VectorBaseInfo).all()
    vector_base_info = [base.name for base in vectorbase_infos]
    session.close()
    return vector_base_info

# 删除VectorBaseInfo


def delete_vector_base_info(name):
    session = Session()
    session.query(VectorBaseInfo).filter(
        VectorBaseInfo.name == name).delete()
    session.commit()
    session.close()

# 判断VectorBase是否存在


def vector_base_exists(name):
    session = Session()
    vectorbase_info = session.query(VectorBaseInfo).filter(
        VectorBaseInfo.name == name).first()
    session.close()
    return vectorbase_info is not None

# 按名字获取单个向量库信息


def get_vector_base_info_by_name(name):
    session = Session()
    vectorbase_info = session.query(VectorBaseInfo).filter(
        VectorBaseInfo.name == name).first()
    session.close()
    return vectorbase_info

# 更新向量库描述


def update_vector_base_detail(vector_base_info: VectorBaseInfo):
    session = Session()
    session.merge(vector_base_info)
    session.commit()
    session.close()


""" LLM会话操作 """

""" 获取所有会话 """


def get_all_chat_session_name():
    session = Session()
    chat_sessions = session.query(ChatSession).all()
    chat_session_names = [chat_session.name for chat_session in chat_sessions]
    session.close()
    return chat_session_names


""" 对话记录保存 """


def save_message_by_chat_session_name(chat_session_name: str, message: dict):
    session = Session()
    chat_session = session.query(ChatSession).filter(
        ChatSession.name == chat_session_name).first()
    message_obj = Message(
        chat_session_id=chat_session.id,
        role=message['role'],
        content=message['content']
    )
    session.add(message_obj)
    session.commit()
    session.close()


""" 按会话名字获取对话消息 """


def get_messages_by_chat_session_name(name):
    session = Session()
    chat_session = session.query(ChatSession).filter(
        ChatSession.name == name).first()
    messages = [{'role': message.role, 'content': message.content}
                for message in chat_session.messages]
    session.close()
    return messages


""" 查看会话是否存在 """


def chat_session_exists(name):
    session = Session()
    chat_session = session.query(ChatSession).filter(
        ChatSession.name == name).first()
    session.close()
    return chat_session is not None


""" 保存会话并返回会话名字 """


def save_chat_session_return_name():
    chat_session = ChatSession()
    session = Session()
    session.add(chat_session)
    session.commit()
    chat_session_name = chat_session.name
    session.close()
    return chat_session_name


""" 删除会话(同时级联删除会话内的对话记录) """


def delete_chat_session(name):
    print(f"\nname:{name}\n")
    session = Session()
    chat_session = session.query(ChatSession).filter(
        ChatSession.name == name).first()
    session.delete(chat_session)
    session.commit()
    session.close()


""" 更新会话名字 """


def update_chat_session_name(name, new_name):
    session = Session()
    chat_session = session.query(ChatSession).filter(
        ChatSession.name == name).first()
    chat_session.name = new_name
    session.commit()
    session.close()
