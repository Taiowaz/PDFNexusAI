from Pinecone_Manager import api_pinecone
from Embedding_Converter.api import api_embedding


# 从Pinecone中检索文本


def retrieve(vectorbase_name: str, text: str) -> list:
    vector = api_embedding.get_single_embedding(text)
    text_list = api_pinecone.query(vectorbase_name, vector)
    return text_list
