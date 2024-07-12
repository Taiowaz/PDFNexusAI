from dashscope import BatchTextEmbedding
import dashscope
import json
import tempfile
import os
import requests
import gzip
from http import HTTPStatus

""" 批量处理文本转向量 """


def get_batch_embeddings(texts_url: str) -> list:
    rsp = BatchTextEmbedding.call(
        model=BatchTextEmbedding.Models.text_embedding_async_v1,
        url=texts_url,
        text_type="document"
    )
    if rsp.status_code == HTTPStatus.OK:
        # 获取向量url
        return rsp.output.url
    else:
        print(rsp)
        return []


""" 单个文本转向量 """


def get_single_embedding(text: str) -> list:
    resp = dashscope.TextEmbedding.call(
        model=dashscope.TextEmbedding.Models.text_embedding_v2,
        input=text,
    )
    if resp.status_code == HTTPStatus.OK:
        return resp.output["embeddings"][0]["embedding"]
    else:
        print(resp)
