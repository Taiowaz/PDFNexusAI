import os
import shutil
from PDF_Processor import pdf_parser
from Embedding_Converter import conversion
from Pinecone_Manager import api_pinecone
import concurrent.futures
from LLM import chat

# 报告处理任务


def process_pdf_vector(vector_name: str, pdf_file: str):
    # 对报告进行分割处理
    text_list = pdf_parser.parse_pdf(pdf_file)
    # 批量转换文本为向量
    embedding_list = conversion.convert_batch(text_list)

    # 对文本与对应向量进行一个组合
    text_embedding_list = []
    for text, embedding in zip(text_list, embedding_list):
        text_embedding_list.append(
            {
                "text": text,
                "embedding": embedding
            }
        )
    # 存入向量数据库中
    api_pinecone.upsert(vector_name, text_embedding_list)
    # 打印日志
    print(f"\nIn stock: {pdf_file}\n")


# 多线程处理PDF文件


def process_pdf_vectorbase_in_threads(vector_name: str, pdf_folder: str):
    # 创建线程池
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # 将处理PDF文件的任务提交给线程池
        futures = [
            executor.submit(
                process_pdf_vector,
                vector_name,
                os.path.join(pdf_folder, pdf_name)
            )
            for pdf_name in os.listdir(pdf_folder)
        ]
    # 等待所有任务完成
    executor.shutdown(wait=True)
    # 检查并处理异常
    for future in futures:
        try:
            future.result()  # 这会抛出异常，如果任务中有任何异常
        except Exception as e:
            print(f"An error occurred while processing a PDF: {e}")
    # 删除文件夹
    shutil.rmtree(pdf_folder)

