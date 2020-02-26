import exrex
from . import models
from django.test import TestCase, Client
from django.http import QueryDict
from django.test.utils import setup_test_environment

"""
本项目可喜可贺地引入tests模块！
yyy老师曾曰：开发的第一步是做先做好测试！
"""


class MessagesModelTests(TestCase):
    """
    用于测试Messages模块
    """

    c = Client()

    def setUp(self):
        """
        初始化测试数据库
        """
        for i in range(10):
            #email = exrex.getone(r"^([A-Za-z0-9_\-\.\u4e00-\u9fa5])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,8})$")
            #理论上邮箱地址是可以包含中文字符的，但是用完整正则规则生成的邮箱地址太过鬼畜所以只用英文字符生成
            email = exrex.getone(r"^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,8})$")
            phonenumber = exrex.getone(r"1[34578][0-9]{9}$")
            password = "mimajiusuiyile123!"
            user = models.User.objects.create(
                email = email,
                phonenumber = phonenumber,
                password = password)
            user.save()

    def test_put_messages_works_successfully(self):
        """
        用于测试发送信息是否正常工作
        """
        request_data = {
            "user_id": 1,
            "title": "rua",
            "content": "ruarua",
            "position": {
                "pos_x": 63.9734911653,
                "pos_y": 86.36421952785102
            },
            "mentioned": [
                {
                "user_id": 2
                },
                {
                "user_id": 3
                }
            ],
            "img": [
                {
                "image_url": ""
                }
            ]
        }
        response = self.c.post('/ww/messages/', data = request_data, content_type = 'application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['state']['msg'], 'successful')
        self.assertGreaterEqual(response.json()['data']['msg_id'], 1)
        