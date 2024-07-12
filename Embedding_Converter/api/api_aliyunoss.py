import oss2

from oss2.credentials import EnvironmentVariableCredentialsProvider

""" 上传文本文件并返回url """
def upload_oss(text_list:list):
    # 获取访问凭证
    auth = oss2.ProviderAuth(EnvironmentVariableCredentialsProvider())
    
    # Bucket所在地域对应Endpoint
    endpoint = "https://oss-cn-beijing.aliyuncs.com"
    
    # Bucket名称
    bucket = oss2.Bucket(auth, endpoint, 'unprocessed-text')
    # 文本列表转字符串，文本元素间换行符分隔
    text_content = '\n'.join(text_list)

    object_name = "text_list.txt"
    bucket.put_object(object_name,text_content)
    # 获取文件url
    url = bucket.sign_url('GET', object_name, 3600)
    return url;


