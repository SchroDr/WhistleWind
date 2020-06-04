import requests
from . import models,
from aip import AipContentCensor
from aip import AipImageCensor

'''
白嫖版本，每天大概50000此请求
现在用的jhc的百度的，也可以注册白嫖
https://ai.baidu.com/tech/textcensoring

conclusionType:可取值1、2、3、4，分别代表1：合规，2：不合规，3：疑似，4：审核失败
'''

class Monitoring():

    APP_ID = '16206995'
    API_KEY = 'D4GGTm9oiDePu3GG9mMYszWu'
    SECRET_KEY = 'Zz46qd8P1eIdXwksCr3ZSMpILlnPE9EG'

    def __init__(self):
        self.client = AipContentCensor(self.APP_ID, self.API_KEY, self.SECRET_KEY)

    def get_file_content(self, filePath):
        return open(filePath, 'rb').read()

    def AipContentCensoR(self, strContent): 
        data = {'text': str(strContent)}
        url = 'https://aip.baidubce.com/rest/2.0/solution/v1/text_censor/v2/user_defined'
        res = self.client.post(url=url, data=data)
        return res['conclusionType']


    def AipImageCensoR(self, filePath):
        result = self.client.imageCensorUserDefined(
            self.get_file_content(filePath))
        return result['conclusionType']

    def testUntestedImages(self):
        images = models.Image.objects.filter(tested=False)
        for image in images:
            image.conclusionType = self.AipImageCensoR(image.url)
            image.tested = True
            image.save()


    def testUntestedMessages(self):
        messages = models.Message.objects.filter(tested=False)
        for message in messages:
            message.conclusionType = self.AipImageCensoR(message.content)
            message.tested = True
            if message.conclusionType == 2:
                message.deleted = 1
            message.save()

    def testUntestedComments(self):
        comments = models.Comment.objects.filter(tested=False)
        for comment in comments:
            comment.conclusionType = self.AipImageCensoR(comment.content)
            comment.tested = True
            if comment.conclusionType == 2:
                comment.deleted = 1
            comment.save()

def start():
    monitor = Monitoring()
    monitor.testUntestedComments()
    monitor.testUntestedImages()
    monitor.testUntestedMessages()