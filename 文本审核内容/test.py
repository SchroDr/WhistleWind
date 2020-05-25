import requests
from aip import AipContentCensor
from aip import AipImageCensor
'''
白嫖版本，每天大概50000此请求
现在用的jhc的百度的，也可以注册白嫖
https://ai.baidu.com/tech/textcensoring
'''


def get_file_content(filePath):
    return open(filePath, 'rb').read()


APP_ID = '16206995'
API_KEY = 'D4GGTm9oiDePu3GG9mMYszWu'
SECRET_KEY = 'Zz46qd8P1eIdXwksCr3ZSMpILlnPE9EG'

# client = AipContentCensor(APP_ID, API_KEY, SECRET_KEY)
# data = {'text': "你好"}
# url = 'https://aip.baidubce.com/rest/2.0/solution/v1/text_censor/v2/user_defined'
# res = client.post(url=url, data=data)
# print(res)

client = AipImageCensor(APP_ID, API_KEY, SECRET_KEY)
result = client.imageCensorUserDefined(
    get_file_content('/Users/lvlaxjh/code/ww/文本审核内容/11.png'))
# result = client.imageCensorUserDefined('http://www.example.com/image.jpg')
print(result)
