# 批量转换向量
from Embedding_Converter.api import api_embedding
from Embedding_Converter.api import api_aliyunoss
import gzip
import json
import os
import tempfile
import requests


def convert_batch(textlist: list):
    # 上传文本文件
    url = api_aliyunoss.upload_oss(textlist)
    # 获取向量url
    embedding_url = api_embedding.get_batch_embeddings(url)
    # 获取向量列表
    embedding_list = get_embeddings_from_url(embedding_url)
    return embedding_list


# 从url获取向量列表
def get_embeddings_from_url(url: str) -> list:
    # 下载压缩包
    response = requests.get(url)
    with open(os.path.join(tempfile.gettempdir(), "embeddings_resp.txt.gz"), 'wb') as f:
        f.write(response.content)

    # 解压
    with gzip.open(os.path.join(tempfile.gettempdir(), "embeddings_resp.txt.gz"), 'rb') as f_in:
        with open(os.path.join(tempfile.gettempdir(), 'embeddings_resp.txt'), 'wb') as f_out:
            f_out.write(f_in.read())

    # 每行作为一个JSON回应，进行读取
    resp_list = []
    with open(os.path.join(tempfile.gettempdir(), 'embeddings_resp.txt'), 'r') as f:
        for line in f:
            resp_list.append(json.loads(line.strip()))

    embedding_list = []
    for resp in resp_list:
        embedding = resp["output"]["embedding"]
        embedding_list.append(embedding)

    return embedding_list


# 获取单个用户输入文本的向量


def convert_single(text: str):
    return api_embedding.get_single_embedding(text)
