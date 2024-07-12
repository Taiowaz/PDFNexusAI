# 根据相关内容构建提示词
from Embedding_Converter import conversion
from Pinecone_Manager import retriever

# 用于增强输出的提示词


def create_prompt_for_input(content: str, vectorbase_name):
    # 数字转英文
    def number_to_words(n):
        num_to_word = {
            1: 'one',
            2: 'two',
            3: 'three',
            4: 'four',
            5: 'five',
            6: 'six',
            7: 'seven',
            8: 'eight',
            9: 'nine',
            10: 'ten'
        }
        return num_to_word.get(n, 'Number out of range')

    # 获取相关文本列表
    text_list = retriever.retrieve(vectorbase_name, content)
    prompt = ""
    i = 1
    for text in text_list:
        prompt += "This is the "+number_to_words(i)+" information:"+text + "//"
        i += 1

    # 构建输入内容
    content = f'''
    You are a helpful assistant,
    This is my question:
    {content}
    The following is relevant text.
    Please judge whether the question is related to the relevant text
    If it is not relevant, please ignore the text provided and answer the question directly yourself
    If relevant, answer in conjunction with the text provided
    {prompt}
    '''

    return content

# 用于判断是否需要查询知识库


def create_prompt_is_query(current_input, vectorbase_name: str):
    prompt = f'''
    Current input content: {current_input}
    This is my current knowledge base: {vectorbase_name}
    Constraints:
    1. Please determine whether the input content is related to the knowledge base name.
    2. Your answer must be either 'yes' or 'no'.
    3. No period needed.
    '''
    return prompt
