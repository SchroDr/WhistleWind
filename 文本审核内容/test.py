import requests
from aip import AipContentCensor
from aip import AipImageCensor
'''
白嫖版本，每天大概50000此请求
现在用的jhc的百度的，也可以注册白嫖
https://ai.baidu.com/tech/textcensoring

conclusionType:可取值1、2、3、4，分别代表1：合规，2：不合规，3：疑似，4：审核失败
'''


def get_file_content(filePath):
    return open(filePath, 'rb').read()


APP_ID = '16206995'
API_KEY = 'D4GGTm9oiDePu3GG9mMYszWu'
SECRET_KEY = 'Zz46qd8P1eIdXwksCr3ZSMpILlnPE9EG'


def AipContentCensoR(strContent):
    client = AipContentCensor(APP_ID, API_KEY, SECRET_KEY)
    data = {'text': str(strContent)}
    url = 'https://aip.baidubce.com/rest/2.0/solution/v1/text_censor/v2/user_defined'
    res = client.post(url=url, data=data)
    return res['conclusionType']
    # return res  # dict


def AipImageCensoR(filePath):
    client = AipImageCensor(APP_ID, API_KEY, SECRET_KEY)
    result = client.imageCensorUserDefined(
        get_file_content(filePath))
    # result = client.imageCensorUserDefined('http://www.example.com/image.jpg')
    #print(result)
    return result['conclusionType']
