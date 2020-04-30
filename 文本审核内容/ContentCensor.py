import requests
from aip import AipContentCensor

'''
白嫖版本，每天大概50000此请求
现在用的jhc的百度的，也可以注册白嫖
https://ai.baidu.com/tech/textcensoring
'''
APP_ID = '16206995'
API_KEY = 'D4GGTm9oiDePu3GG9mMYszWu'
SECRET_KEY = 'Zz46qd8P1eIdXwksCr3ZSMpILlnPE9EG'

client = AipContentCensor(APP_ID, API_KEY, SECRET_KEY)
data = {'text': "你好"}
url = 'https://aip.baidubce.com/rest/2.0/solution/v1/text_censor/v2/user_defined'
res = client.post(url=url, data=data)
print(res)
