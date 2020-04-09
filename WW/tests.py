import exrex
import random
import demjson
from . import models
from datetime import datetime, timedelta, timezone
from django.test import TestCase, Client
from django.http import QueryDict
from django.test.utils import setup_test_environment
from django.core.cache import cache
from django.db import transaction

"""
本项目可喜可贺地引入tests模块！
yyy老师曾曰：开发的第一步是做先做好测试！
"""


def createTestDatabase():
    """
    初始化测试数据库
    向测试数据库中添加10个用户信息、每个用户有5条信息，每个信息有5条评论
    """
    # 创建2个tag
    tag_1 = models.Tag.objects.create(tag="C")
    tag_1.save()
    tag_2 = models.Tag.objects.create(tag="Python")
    tag_2.save()
    # 创建10个用户
    for i in range(10):
        #email = exrex.getone(r"^([A-Za-z0-9_\-\.\u4e00-\u9fa5])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,8})$")
        # 理论上邮箱地址是可以包含中文字符的，但是用完整正则规则生成的邮箱地址太过鬼畜所以只用英文字符生成
        email = exrex.getone(
            r"^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,8})$")
        phonenumber = exrex.getone(r"1[34578][0-9]{9}$")
        password = "mimajiusuiyile123!"
        user = models.User.objects.create(
            email=email,
            phonenumber=phonenumber,
            password=password)
        user.save()
    users = models.User.objects.all()
    # 为每个用户增加10条消息
    for user in users:
        for i in range(5):
            message = models.Message.objects.create(
                pos_x=63.9734911653,
                pos_y=86.36421952785102,
                title="Test",
                content="Heeeeeeeeeeeeeeeelo",
                author=user
            )
            message.tag.add(tag_1)
            message.tag.add(tag_2)
            for mention_user in random.sample(list(users), 3):
                message.mention.add(mention_user)
            message.save()
    messages = models.Message.objects.all()
    # 为每条信息增加10条评论，3张图片，5个点赞，5个点踩
    for message in messages:
        for i in range(5):
            user = random.choice(users)
            comment = models.Comment.objects.create(
                msg=message,
                author=user,
                content="Ruaaaaaaaa"
            )
            comment.save()
        for i in range(3):
            messageImage = models.MessageImage.objects.create(
                message=message, img='media/pic/rua.jpg'
            )
            messageImage.save()
        for user in random.sample(list(users), 5):
            message.like += 1
            message.who_like.add(user)
            message.save()
        for user in random.sample(list(users), 5):
            message.dislike += 1
            message.who_dislike.add(user)
            message.save()
    comments = models.Comment.objects.all()
    # 为每条评论增加5个点赞，2个子评论
    for comment in comments:
        for user in random.sample(list(users), 5):
            comment.like += 1
            comment.who_like.add(user)
            comment.save()
            child_comment = models.Comment.objects.create(
                msg = comment.msg,
                author = user,
                type = 'child',
                reply_to = comment.author,
                parent_comment = comment
            )
            child_comment.save()

    # 为每个用户增加9个关注
    for user in users:
        for follow in users:
            followship = models.Followship.objects.create(
                followed_user=follow,
                fan=user
            )
            followship.save()


class UsersModelTests(TestCase):
    """
    用于测试Users模块
    """

    c = Client()

    def setUp(self):
        createTestDatabase()

    def test_register_works_successfully(self):
        """正常注册的情况"""
        request_data = {
            "phone_number": exrex.getone(r"1[34578][0-9]{9}$"),
            "veri_code": exrex.getone(r"\d{4}"),
            "password": exrex.getone(r"[A-Za-z0-9_]{6,18}")
        }
        response = self.c.post(
            '/ww/users/', data=request_data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['state']['msg'], 'successful')
        self.assertGreaterEqual(response.json()['data']['user_id'], 1)

    def test_register_works_with_registered_number(self):
        """使用已注册号码注册的情况"""
        user = models.User.objects.filter()[0]
        request_data = {
            "phone_number": user.phonenumber,
            "veri_code": exrex.getone(r"\d{4}"),
            "password": exrex.getone(r"[A-Za-z0-9_]{6,18}")
        }
        response = self.c.post(
            '/ww/users/', data=request_data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['state']['msg'], 'existed')

    def test_register_works_with_wrong_number(self):
        """使用错误格式的号码注册的情况"""
        request_data = {
            "phone_number": exrex.getone(r"1[34578][0-9]{8}$"),
            "veri_code": exrex.getone(r"\d{4}"),
            "password": exrex.getone(r"[A-Za-z0-9_]{6,18}")
        }
        response = self.c.post(
            '/ww/users/', data=request_data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['state']['msg'], 'wrong')

    def test_get_basic_user_info(self):
        """测试用户的基本信息是否返回正确"""
        user = models.User.objects.all()[0]
        request_data = {
            "user_id": user.id,
            "follows_number": -1,
            "followers_number": -1,
            "messages_number": -1,
            "comments_number": -1,
            "follows_start": 0,
            "followers_start": 0,
            "messages_start": 0,
            "comments_start": 0
        }
        response = self.c.get('/ww/users/', data=request_data,
                              content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['state']['msg'], 'successful')
        self.assertEqual(response.json()['data']
                         ['user_id'], request_data['user_id'])
        self.assertEqual(response.json()['data']
                         ['username'], user.username)
        self.assertEqual(response.json()['data']
                         ['email'], user.email)
        self.assertEqual(response.json()['data']
                         ['phonenumber'], user.phonenumber)
        self.assertEqual(response.json()['data']
                         ['avatar'], user.avatar)
        self.assertEqual(response.json()['data']
                         ['introduction'], user.introduction)
        self.assertEqual(response.json()['data']
                         ['birth_date'], user.birth_date.strftime("%Y-%m-%d"))
        self.assertEqual(response.json()['data']
                         ['gender'], user.gender)
        self.assertEqual(response.json()['data']
                         ['registration_date'], user.registration_date.strftime("%Y-%m-%d"))

    def test_get_basic_user_info_with_wong_id(self):
        """使用错误的id，测试用户的基本信息"""
        user = models.User.objects.all()[0]
        request_data = {
            "user_id": 9999,
            "follows_number": -1,
            "followers_number": -1,
            "messages_number": -1,
            "comments_number": -1,
            "follows_start": 0,
            "followers_start": 0,
            "messages_start": 0,
            "comments_start": 0
        }
        response = self.c.get('/ww/users/', data=request_data,
                              content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['state']['msg'], 'wrong')


    def test_get_user_info_and_messages_info(self):
        """测试用户已发送的信息是否返回正确"""
        user = models.User.objects.all()[0]
        request_data = {
            "user_id": user.id,
            "follows_number": -1,
            "followers_number": -1,
            "messages_number": -1,
            "comments_number": -1,
            "follows_start": 0,
            "followers_start": 0,
            "messages_start": 0,
            "comments_start": 0
        }
        response = self.c.get('/ww/users/', data=request_data,
                              content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['state']['msg'], 'successful')
        message = models.Message.objects.filter(
            id = response.json()['data']['messages'][0]['message_id']
        )[0]
        self.assertEqual(
            response.json()['data']['messages'][0]['title'], message.title
        )
        self.assertEqual(
            response.json()['data']['messages'][0]['content'], message.content
        )
        self.assertEqual(
            response.json()['data']['messages'][0]['like'], message.like
        )
        self.assertEqual(
            response.json()['data']['messages'][0]['dislike'], message.dislike
        )
        self.assertEqual(
            response.json()['data']['messages'][0]['comments_number'], message.comment_set.count()
        )
        self.assertEqual(
            len(response.json()['data']['messages'][0]['images']), message.messageimage_set.count()
        )

    def test_get_user_info_and_comments_info(self):
        """测试用户已发送的评论是否返回正确"""
        user = models.User.objects.all()[0]
        request_data = {
            "user_id": user.id,
            "follows_number": -1,
            "followers_number": -1,
            "messages_number": -1,
            "comments_number": -1,
            "follows_start": 0,
            "followers_start": 0,
            "messages_start": 0,
            "comments_start": 0
        }
        response = self.c.get('/ww/users/', data=request_data,
                              content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['state']['msg'], 'successful')
        comment = models.Comment.objects.filter(
            id = response.json()['data']['comments'][0]['comment_id']
        )[0]
        self.assertEqual(
            response.json()['data']['comments'][0]['content'], comment.content
        )

    def test_get_user_info_and_followers_info(self):
        """测试用户的粉丝是否返回正确"""
        user = models.User.objects.all()[0]
        request_data = {
            "user_id": user.id,
            "follows_number": -1,
            "followers_number": -1,
            "messages_number": -1,
            "comments_number": -1,
            "follows_start": 0,
            "followers_start": 0,
            "messages_start": 0,
            "comments_start": 0
        }
        response = self.c.get('/ww/users/', data=request_data,
                              content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['state']['msg'], 'successful')
        follower = models.User.objects.filter(
            id = response.json()['data']['followers'][0]['user_id']
        )[0]
        self.assertEqual(
            response.json()['data']['followers'][0]['username'], follower.username
        )
        self.assertEqual(
            response.json()['data']['followers'][0]['avatar'], follower.avatar
        )

    def test_get_user_info_and_follows_info(self):
        """测试用户的关注是否返回正确"""
        user = models.User.objects.all()[0]
        request_data = {
            "user_id": user.id,
            "follows_number": -1,
            "followers_number": -1,
            "messages_number": -1,
            "comments_number": -1,
            "follows_start": 0,
            "followers_start": 0,
            "messages_start": 0,
            "comments_start": 0
        }
        response = self.c.get('/ww/users/', data=request_data,
                              content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['state']['msg'], 'successful')
        follow = models.User.objects.filter(
            id = response.json()['data']['follows'][0]['user_id']
        )[0]
        self.assertEqual(
            response.json()['data']['follows'][0]['username'], follow.username
        )
        self.assertEqual(
            response.json()['data']['follows'][0]['avatar'], follow.avatar
        )

    def test_get_user_info_and_various_number(self):
        """测试用户的各类数据是否正确"""
        user = models.User.objects.all()[0]
        request_data = {
            "user_id": user.id,
            "follows_number": -1,
            "followers_number": -1,
            "messages_number": -1,
            "comments_number": -1,
            "follows_start": 0,
            "followers_start": 0,
            "messages_start": 0,
            "comments_start": 0
        }
        response = self.c.get('/ww/users/', data=request_data,
                              content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['state']['msg'], 'successful')
        self.assertEqual(
            response.json()['data']['follows_number'], user.follows.count())
        self.assertEqual(
            response.json()['data']['followers_number'], user.follow_set.count())
        self.assertEqual(
            response.json()['data']['messages_number'], user.message_set.count())
        self.assertEqual(
            response.json()['data']['comments_number'], user.comment_set.count())

    def test_get_all_user_info_works_successfully(self):
        """获取所有用户的所有信息的情况，测试能否正确返回应有的数量"""
        user = models.User.objects.all()[0]
        request_data = {
            "user_id": user.id,
            "follows_number": -1,
            "followers_number": -1,
            "messages_number": -1,
            "comments_number": -1,
            "follows_start": 0,
            "followers_start": 0,
            "messages_start": 0,
            "comments_start": 0
        }
        response = self.c.get('/ww/users/', data=request_data,
                              content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['state']['msg'], 'successful')
        self.assertEqual(
            len(response.json()['data']['follows']), user.follows.count())
        self.assertEqual(
            len(response.json()['data']['followers']), user.follow_set.count())
        self.assertEqual(
            len(response.json()['data']['messages']), user.message_set.count())
        self.assertEqual(
            len(response.json()['data']['comments']), user.comment_set.count())
        


    def test_get_part_user_messages_works_successfully(self):
        """获取用户的部分信息的情况，测试能否正确返回应有的数量"""
        user = models.User.objects.all()[0]
        request_data = {
            "user_id": user.id,
            "follows_number": 3,
            "followers_number": 3,
            "messages_number": 3,
            "comments_number": 3,
            "follows_start": 0,
            "followers_start": 0,
            "messages_start": 0,
            "comments_start": 0
        }

        response = self.c.get('/ww/users/', data=request_data,
                              content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['state']['msg'], 'successful')
        self.assertEqual(response.json()['data']
                         ['user_id'], request_data['user_id'])
        self.assertEqual(len(response.json()['data']['follows']), 3)
        self.assertEqual(len(response.json()['data']['followers']), 3)
        self.assertEqual(len(response.json()['data']['messages']), 3)
        self.assertEqual(len(response.json()['data']['comments']), 3)

    def test_get_minimal_user_messages_works_successfully(self):
        """获取用户的最少信息的情况，测试能否正确返回应有的数量"""
        user = models.User.objects.all()[0]
        request_data = {
            "user_id": user.id,
            "follows_number": 0,
            "followers_number": 0,
            "messages_number": 0,
            "comments_number": 0,
            "follows_start": 0,
            "followers_start": 0,
            "messages_start": 0,
            "comments_start": 0
        }
        response = self.c.get('/ww/users/', data=request_data,
                              content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['state']['msg'], 'successful')
        self.assertEqual(response.json()['data']
                         ['user_id'], request_data['user_id'])
        self.assertEqual(len(response.json()['data']['follows']), 0)
        self.assertEqual(len(response.json()['data']['followers']), 0)
        self.assertEqual(len(response.json()['data']['messages']), 0)
        self.assertEqual(len(response.json()['data']['comments']), 0)


    def test_update_user_messages_works_successfully(self):
        """使用所有参数，正常更新用户信息的情况"""
        user = models.User.objects.all()[0]
        request_data = {
            "user_id": user.id,
            "username": "张三",
            "email": exrex.getone(r"^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,8})$"),
            "phonenumber": exrex.getone(r"1[34578][0-9]{9}$"),
            "introduction": "HAHAHA😀",
            "avatar": "media/pic/029jozv8jp.png",
            "gender": "male",
            "birth_date": "1990-01-31"
        }
        response = self.c.put('/ww/users/', data=request_data,
                              content_type='application/json')
        try:
            with transaction.atomic():
                user.refresh_from_db()
        except Exception as e:
            print("WTF")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['state']['msg'], 'successful')
        self.assertEqual(response.json()['data']
                         ['user_id'], request_data['user_id'])
        self.assertEqual(user.username, request_data['username'])
        self.assertEqual(user.email, request_data['email'])
        self.assertEqual(user.phonenumber, request_data['phonenumber'])
        self.assertEqual(user.introduction, request_data['introduction'])
        self.assertEqual(user.avatar, request_data['avatar'])
        self.assertEqual(user.gender, request_data['gender'])
        self.assertEqual(user.birth_date.strftime("%Y-%m-%d"), request_data['birth_date'])

    def test_update_user_messages_works_with_wrong_id(self):
        """使用错误的id，更新用户信息的情况"""
        user = models.User.objects.all()[0]
        request_data = {
            "user_id": 99999,
            "username": "张三",
            "email": exrex.getone(r"^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,8})$"),
            "phonenumber": exrex.getone(r"1[34578][0-9]{9}$"),
            "introduction": "HAHAHA😀",
            "avatar": "media/pic/029jozv8jp.png",
            "gender": "male",
            "birth_date": "1990-01-31"
        }
        response = self.c.put('/ww/users/', data=request_data,
                              content_type='application/json')
        try:
            with transaction.atomic():
                user.refresh_from_db()
        except Exception as e:
            print("WTF")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['state']['msg'], 'wrong')
    
    def test_update_user_messages_works_successfully_with_part_params(self):
        """使用部分参数，正常更新用户信息的情况"""
        user = models.User.objects.all()[0]
        request_data = {
            "username": "张三",
            "email": exrex.getone(r"^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,8})$"),
            "phonenumber": exrex.getone(r"1[34578][0-9]{9}$"),
            "introduction": "HAHAHA😀",
            "avatar": "media/pic/029jozv8jp.png",
            "gender": "male",
            "birth_date": "1990-01-31"
        }
        keys = random.sample(request_data.keys(), 3)
        for key in keys:
            del request_data[key]
        request_data["user_id"] = user.id
        response = self.c.put('/ww/users/', data=request_data,
                              content_type='application/json')
        try:
            with transaction.atomic():
                user.refresh_from_db()
        except Exception as e:
            print("WTF")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['state']['msg'], 'successful')
        self.assertEqual(response.json()['data']
                         ['user_id'], request_data['user_id'])


class MessagesModelTests(TestCase):
    """
    用于测试Messages模块
    """

    c = Client()

    def setUp(self):
        createTestDatabase()

    def test_post_messages_works_successfully(self):
        """正常发送信息"""
        user = models.User.objects.all()[0]
        request_data = {
            "user_id": user.id,
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
            "images": [
                {
                    "image_url": "media/pic/rua.jpg"
                },
                {
                    "image_url": "media/pic/rua.jpg"
                },
                {
                    "image_url": "media/pic/rua.jpg"
                }
            ],
            "tags": [
                {
                    "tag": "LOL"
                },
                {
                    "tag": "GOG"
                }
            ],
            "device": "NOKIA"
        }
        response = self.c.post(
            '/ww/messages/', data=request_data, content_type='application/json')
        message = models.Message.objects.filter(
            id=response.json()['data']['msg_id'])[0]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['state']['msg'], 'successful')
        self.assertGreaterEqual(response.json()['data']['msg_id'], 1)
        self.assertEqual(len(message.messageimage_set.all()), 3)
        self.assertEqual(message.tag.count(), len(request_data['tags']))
        self.assertEqual(message.mention.count(), len(request_data['mentioned']))
        self.assertEqual(message.device, request_data['device'])

    def test_post_messages_works_with_non_existent_id(self):
        """使用错误的id发送信息"""
        request_data = {
            "user_id": 99999,
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
            "images": [
                {
                    "image_url": "media/pic/rua.jpg"
                },
                {
                    "image_url": "media/pic/rua.jpg"
                },
                {
                    "image_url": "media/pic/rua.jpg"
                }
            ],
            "tags": [
                {
                    "tag": "LOL"
                },
                {
                    "tag": "GOG"
                }
            ],
            "device": "NOKIA"
        }
        response = self.c.post(
            '/ww/messages/', data=request_data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['state']['msg'], 'wrong')

    def test_post_messages_works_with_deleted_id(self):
        """使用已删除的id发送信息"""
        user = models.User.objects.all()[0]
        request_data = {
            "user_id": user.id,
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
            "images": [
                {
                    "image_url": "media/pic/rua.jpg"
                },
                {
                    "image_url": "media/pic/rua.jpg"
                },
                {
                    "image_url": "media/pic/rua.jpg"
                }
            ],
            "tags": [
                {
                    "tag": "LOL"
                },
                {
                    "tag": "GOG"
                }
            ],
            "device": "NOKIA"
        }
        user.deleted = 1
        user.save()
        response = self.c.post(
            '/ww/messages/', data=request_data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['state']['msg'], 'deleted')
        user.deleted = 0
        user.save()


    def test_get_messages_works_successfully(self):
        """用于测试获取信息详情是否工作正常"""
        message = models.Message.objects.all()[0]
        request_data = {
            "msg_id": message.id,
            "who_like_limit": 10,
            "who_dislike_limit": 10
        }
        response = self.c.get(
            '/ww/messages/', data=request_data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['state']['msg'], 'successful')
        self.assertEqual(response.json()['data']
                         ['msg_id'], request_data['msg_id'])
        self.assertEqual(response.json()['data']
                         ['title'], message.title)
        self.assertEqual(response.json()['data']
                         ['content'], message.content)
        self.assertEqual(response.json()['data']
                         ['position']['pos_x'], str(message.pos_x))
        self.assertEqual(response.json()['data']
                         ['position']['pos_y'], str(message.pos_y))
        self.assertEqual(response.json()['data']
                         ['author']['author_id'], message.author.id)
        self.assertEqual(response.json()['data']
                         ['author']['username'], message.author.username)
        self.assertEqual(response.json()['data']
                         ['author']['avatar'], message.author.avatar)
        self.assertEqual(response.json()['data']
                         ['like'], str(message.like))
        user_like = models.User.objects.filter(
            id=response.json()['data']['who_like'][0]['user_id']
        )[0]
        self.assertEqual(
            response.json()['data']['who_like'][0]['username'], user_like.username
        )
        self.assertEqual(
            response.json()['data']['who_like'][0]['avatar'], user_like.avatar
        )
        self.assertEqual(
            response.json()['data']['add_date'], message.add_date.astimezone(
                        timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M:%S")
        )
        self.assertEqual(
            response.json()['data']['mod_date'], message.mod_date.astimezone(
                        timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M:%S")
        )
        comment = models.User.objects.filter(
            id=response.json()['data']['comments'][0]['comment_id']
        )[0]
        self.assertEqual(
            response.json()['data']['comments'][0]['content'], comment.content
        )
        self.assertEqual(
            response.json()['data']['comments'][0]['like'], str(comment.like)
        )
        comment_author = models.User.objects.filter(
            id=response.json()['data']['comments'][0]['author']['author_id']
        )[0]
        self.assertEqual(
            response.json()['data']['comments'][0]['author']['username'], comment_author.username
        )
        self.assertEqual(
            response.json()['data']['comments'][0]['author']['username'], comment_author.avatar
        )
        self.assertEqual(
            len(response.json()['data']['images']), message.messageimage_set.count()
        )
        self.assertEqual(
            len(response.json()['data']['mentioned']), message.mention.count()
        )
        self.assertEqual(
            len(response.json()['data']['tags']), message.tag.count()
        )
        self.assertEqual(
            response.json()['data']['device'], message.device
        )


    def test_get_messages_works_with_wrong_id(self):
        """使用错误id的情况"""
        message = models.Message.objects.all()[0]
        request_data = {
            "msg_id": 99999,
            "who_like_limit": 10,
            "who_dislike_limit": 10
        }
        response = self.c.get(
            '/ww/messages/', data=request_data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['state']['msg'], 'wrong')

    def test_get_messages_works_with_deleted_id(self):
        """使用已删除id的情况"""
        message = models.Message.objects.all()[0]
        request_data = {
            "msg_id": 99999,
            "who_like_limit": 10,
            "who_dislike_limit": 10
        }
        message.deleted = 1
        message.save()
        response = self.c.get(
            '/ww/messages/', data=request_data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['state']['msg'], 'deleted')
        message.deleted = 0
        message.save()


    def test_put_messages_works_successfully(self):
        """用于测试修改信息是否工作正常"""
        request_data = {
            "msg_id": models.Message.objects.all()[0].id,
            "title": "NewTitle",
            "content": "NewContent",
            "mentioned": [
                {
                    "user_id": 2
                }
            ],
            "images": [
                {
                    "image_url": "/media/pic/rua.jpg"
                },
                {
                    "image_url": "/media/pic/rua.jpg"
                }
            ],
            "device": "MOTOR",
            "tags": [
                {
                    "tag": "CYBERPUPNK"
                },
                {
                    "tag": "MORI"
                }
            ]
        }
        response = self.c.put(
            '/ww/messages/', data=request_data, content_type='application/json')
        message = models.Message.objects.filter(
            id=response.json()['data']['msg_id'])[0]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['state']['msg'], 'successful')
        self.assertEqual(response.json()['data']
                         ['msg_id'], request_data['msg_id'])
        self.assertEqual(len(message.messageimage_set.all()), len(request_data['images']))
        self.assertEqual(len(message.tag.all()), len(request_data['tags']))
        self.assertEqual(message.device, request_data['device'])

    def test_put_messages_works_with_wrong_id(self):
        """使用错误id的情况"""
        request_data = {
            "msg_id": 99999,
            "title": "NewTitle",
            "content": "NewContent",
            "mentioned": [
                {
                    "user_id": 2
                }
            ],
            "images": [
                {
                    "image_url": "/media/pic/rua.jpg"
                },
                {
                    "image_url": "/media/pic/rua.jpg"
                }
            ],
            "device": "MOTOR",
            "tags": [
                {
                    "tag": "CYBERPUPNK"
                },
                {
                    "tag": "MORI"
                }
            ]
        }
        response = self.c.put(
            '/ww/messages/', data=request_data, content_type='application/json')
        message = models.Message.objects.filter(
            id=response.json()['data']['msg_id'])[0]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['state']['msg'], 'wrong')

    def test_put_messages_works_with_deleted_id(self):
        """使用已删除id的情况"""
        message = models.Message.objects.all()[0]
        request_data = {
            "msg_id": message.id,
            "title": "NewTitle",
            "content": "NewContent",
            "mentioned": [
                {
                    "user_id": 2
                }
            ],
            "images": [
                {
                    "image_url": "/media/pic/rua.jpg"
                },
                {
                    "image_url": "/media/pic/rua.jpg"
                }
            ],
            "device": "MOTOR",
            "tags": [
                {
                    "tag": "CYBERPUPNK"
                },
                {
                    "tag": "MORI"
                }
            ]
        }
        message.deleted = 1
        message.save()
        response = self.c.put(
            '/ww/messages/', data=request_data, content_type='application/json')
        message = models.Message.objects.filter(
            id=response.json()['data']['msg_id'])[0]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['state']['msg'], 'deleted')
        message.deleted = 0
        message.save()


    def test_delete_messages_works_successfully(self):
        """用于测试删除信息是否工作正常"""
        request_data = {
            "msg_id": models.Message.objects.all()[0].id
        }
        response = self.c.delete(
            '/ww/messages/', data=request_data, content_type='application/json')
        message = models.Message.objects.filter(
            id=request_data['msg_id']
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['state']['msg'], 'successful')
        self.assertEqual(response.json()['data']
                         ['msg_id'], request_data['msg_id'])
        self.assertEqual(message.deleted, 1)

    def test_delete_messages_works_with_wrong_id(self):
        """使用错误id的情况"""
        request_data = {
            "msg_id": 99999
        }
        response = self.c.delete(
            '/ww/messages/', data=request_data, content_type='application/json')
        message = models.Message.objects.filter(
            id=request_data['msg_id']
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['state']['msg'], 'wrong')

    def test_delete_messages_works_with_deleted_id(self):
        """使用已删除id的情况"""
        request_data = {
            "msg_id": 99999
        }
        response = self.c.delete(
            '/ww/messages/', data=request_data, content_type='application/json')
        message = models.Message.objects.filter(
            id=request_data['msg_id']
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['state']['msg'], 'deleted')


    def test_get_a_set_messages_works_successfully(self):
        """测试能否正确获取一组信息"""
        user = models.User.objects.filter()[0]
        request_data = {
            "pos_x": 63.9734911653,
            "pos_y": 86.36421952785102,
            "width": 2,
            "height": 2,
            "user_id": user.id,
            "number": 18
        }
        response = self.c.get(
            '/ww/messages/set/', data=request_data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['state']['msg'], 'successful')
        self.assertLessEqual(len(response.json()['data']['messages']), 18)

    def test_give_a_like_to_a_message_works_successfully(self):
        """ 测试能否正确点赞"""
        message = models.Message.objects.filter()[0]
        users_liked = message.who_like.all()
        users = models.User.objects.all()
        user = list(filter(lambda u: u not in users_liked, users))[0]
        request_data = {
            "msg_id": message.id,
            "user_id": user.id
        }
        response = self.c.post(
            '/ww/messages/like/', data=request_data, content_type='application/json')
        message.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['state']['msg'], 'successful')
        self.assertEqual(response.json()['data']['msg_id'], message.id)
        self.assertEqual(response.json()['data']['like'], message.like)
        self.assertEqual(response.json()['data']['dislike'], message.dislike)
        self.assertIn(user, message.who_like.all())

    def test_give_two_likes_to_a_message(self):
        """点多次赞的情况"""
        message = models.Message.objects.filter()[0]
        users_liked = message.who_like.all()
        users = models.User.objects.all()
        user = list(filter(lambda u: u not in users_liked, users))[0]
        request_data = {
            "msg_id": message.id,
            "user_id": user.id
        }
        response = self.c.post(
            '/ww/messages/like/', data=request_data, content_type='application/json')
        response = self.c.post(
            '/ww/messages/like/', data=request_data, content_type='application/json')
        message.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['state']['msg'], 'wrong')
        self.assertEqual(response.json()['data']['msg_id'], message.id)
        self.assertEqual(response.json()['data']['like'], message.like)
        self.assertEqual(response.json()['data']['dislike'], message.dislike)
        self.assertIn(user, message.who_like.all())

    def test_give_a_dislike_to_a_message_works_successfully(self):
        """测试能否正确点踩"""
        message = models.Message.objects.filter()[0]
        users_disliked = message.who_dislike.all()
        users = models.User.objects.all()
        user = list(filter(lambda u: u not in users_disliked, users))[0]
        request_data = {
            "msg_id": message.id,
            "user_id": user.id
        }
        response = self.c.post(
            '/ww/messages/dislike/', data=request_data, content_type='application/json')
        message.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['state']['msg'], 'successful')
        self.assertEqual(response.json()['data']['msg_id'], message.id)
        self.assertEqual(response.json()['data']['like'], message.like)
        self.assertEqual(response.json()['data']['dislike'], message.dislike)
        self.assertIn(user, message.who_dislike.all())

    def test_give_two_dislikes_to_a_message(self):
        """点多次踩的情况"""
        message = models.Message.objects.filter()[0]
        users_disliked = message.who_dislike.all()
        users = models.User.objects.all()
        user = list(filter(lambda u: u not in users_disliked, users))[0]
        request_data = {
            "msg_id": message.id,
            "user_id": user.id
        }
        response = self.c.post(
            '/ww/messages/dislike/', data=request_data, content_type='application/json')
        response = self.c.post(
            '/ww/messages/dislike/', data=request_data, content_type='application/json')
        message.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['state']['msg'], 'wrong')
        self.assertEqual(response.json()['data']['msg_id'], message.id)
        self.assertEqual(response.json()['data']['like'], message.like)
        self.assertEqual(response.json()['data']['dislike'], message.dislike)
        self.assertIn(user, message.who_dislike.all())

    # def test_get_all_mentioned_messages_works_successfully(self):
    #     """
    #     TO DO 测试能否正确获取被@的信息
    #     """
    #     user = models.User.objects.filter()[0]
    #     request_data = {
    #         "user_id": user.id,
    #         "time_limit": -1,
    #         "count_limit": -1
    #     }
    #     response = self.c.get(
    #         '/ww/messages/mentioned', data=request_data, content_type='application/json')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.json()['state']['msg'], 'successful')
    #     self.assertEqual(len(response.json()['data']['messages'], len(user.message_set.all())))


class CommentsModelTests(TestCase):
    """
    用于测试Comments模块
    """

    c = Client()

    def setUp(self):
        createTestDatabase()

    def test_post_comments_works_successfully(self):
        """用于测试发送评论是否正常工作"""
        user = models.User.objects.all()[0]
        message = models.Message.objects.all()[0]
        request_data = {
            "user_id": user.id,
            "content": "ruarua",
            "msg_id": message.id
        }
        response = self.c.post(
            '/ww/comments/', data=request_data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['state']['msg'], 'successful')
        self.assertGreaterEqual(response.json()['data']['comment_id'], 1)

    def test_post_comments_works_with_nonexistent_id(self):
        """使用不存在的用户或者信息id发送评论"""
        user = models.User.objects.all()[0]
        message = models.Message.objects.all()[0]
        request_data = {
            "user_id": 99999,
            "content": "ruarua",
            "msg_id": 99999
        }
        response = self.c.post(
            '/ww/comments/', data=request_data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['state']['msg'], 'wrong')
        self.assertGreaterEqual(response.json()['data']['comment_id'], 1)

    def test_post_comments_works_with_deleted_id(self):
        """使用已删除的用户或者信息id发送评论"""
        user = models.User.objects.all()[0]
        message = models.Message.objects.all()[0]
        request_data = {
            "user_id": user.id,
            "content": "ruarua",
            "msg_id": message.id
        }
        user.deleted = 1
        message.deleted = 1
        user.save()
        message.save()
        response = self.c.post(
            '/ww/comments/', data=request_data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['state']['msg'], 'successful')
        self.assertGreaterEqual(response.json()['data']['comment_id'], 1)
        user.deleted = 0
        message.deleted = 0
        user.save()
        message.save()

    def test_post_child_comments_works_successfully(self):
        """用于测试发送子评论是否正常工作"""
        user = models.User.objects.all()[0]
        message = models.Message.objects.all()[0]
        parent_comment = message.comment_set.all()[0]
        request_data = {
            "user_id": user.id,
            "content": "ruarua",
            "msg_id": message.id,
            'parent_comment_id': parent_comment.id,
            'reply_to': parent_comment.author.id
        }
        response = self.c.post(
            '/ww/comments/', data=request_data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['state']['msg'], 'successful')
        self.assertGreaterEqual(response.json()['data']['comment_id'], 1)

    def test_post_child_comments_works_with_nonexistent_id(self):
        """使用不存在的用户或者信息id发送子评论"""
        user = models.User.objects.all()[0]
        message = models.Message.objects.all()[0]
        parent_comment = message.comment_set.all()[0]
        request_data = {
            "user_id": 99999,
            "content": "ruarua",
            "msg_id": 99999,
            'parent_comment_id': 99999,
            'reply_to': 99999
        }
        response = self.c.post(
            '/ww/comments/', data=request_data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['state']['msg'], 'wrong')
        self.assertGreaterEqual(response.json()['data']['comment_id'], 1)

    def test_post_child_comments_works_with_deleted_id(self):
        """使用已删除的用户或者信息id发送子评论"""
        user = models.User.objects.all()[0]
        message = models.Message.objects.all()[0]
        parent_comment = message.comment_set.all()[0]
        request_data = {
            "user_id": user.id,
            "content": "ruarua",
            "msg_id": message.id,
            'parent_comment_id': parent_comment.id,
            'reply_to': parent_comment.author.id
        }
        user.deleted = 1
        message.deleted = 1
        parent_comment.deleted = 1
        user.save()
        message.save()
        parent_comment.save()
        response = self.c.post(
            '/ww/comments/', data=request_data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['state']['msg'], 'successful')
        self.assertGreaterEqual(response.json()['data']['comment_id'], 1)
        user.deleted = 0
        message.deleted = 0
        parent_comment.deleted = 0
        user.save()
        message.save()
        parent_comment.save()


    def test_get_comments_works_successfully(self):
        """用于测试获取评论是否工作正常"""
        comment = models.Comment.objects.filter(type='parent')[0]
        request_data = {
            "comment_id": comment.id
        }
        response = self.c.get(
            '/ww/comments/', data=request_data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['state']['msg'], 'successful')
        self.assertEqual(
            response.json()['data']['comment_id'], request_data['comment_id'])
        self.assertEqual(
            response.json()['data']['author']['author_id'], str(comment.author.id)
        )
        self.assertEqual(
            response.json()['data']['author']['username'], comment.author.username
        )
        self.assertEqual(
            response.json()['data']['author']['avatar'], comment.author.avatar
        )
        self.assertEqual(
            response.json()['data']['msg_id'], str(comment.msg.id)
        )
        self.assertEqual(
            response.json()['data']['content'], comment.content
        )
        self.assertEqual(
            response.json()['data']['like'], comment.like
        )
        user_like = models.User.objects.filter(
            id=response.json()['data']['who_like'][0]['user_id']
        )[0]
        self.assertEqual(
            response.json()['data']['who_like'][0]['username'], user_like.username
        )
        self.assertEqual(
            response.json()['data']['who_like'][0]['avatar'], user_like.avatar
        )
        self.assertEqual(
            response.json()['data']['add_date'], comment.add_date.astimezone(
                        timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M:%S")
        )
        self.assertEqual(
            response.json()['data']['mod_date'], comment.mod_date.astimezone(
                        timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M:%S")
        )
        child_comment = models.Comment.objects.filter(
            id=response.json()['data']['child_comments'][0]['comment_id']
            )[0]
        self.assertEqual(
            response.json()['data']['child_comments'][0]['content'], child_comment.content
        )
        self.assertEqual(
            response.json()['data']['child_comments'][0]['like'], child_comment.like
        )
        self.assertEqual(
            response.json()['data']['child_comments'][0]['author']['author_id'], child_comment.author.id
        )
        self.assertEqual(
            response.json()['data']['child_comments'][0]['author']['username'], child_comment.author.username
        )
        self.assertEqual(
            response.json()['data']['child_comments'][0]['author']['avatar'], child_comment.author.avatar
        )
        

    def test_get_child_comments_works_successfully(self):
        """用于测试获取子评论是否工作正常"""
        comment = models.Comment.objects.filter(type='child')[0]
        request_data = {
            "comment_id": comment.id
        }
        response = self.c.get(
            '/ww/comments/', data=request_data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['state']['msg'], 'successful')
        self.assertEqual(
            response.json()['data']['comment_id'], request_data['comment_id'])
        self.assertEqual(
            response.json()['data']['author']['author_id'], str(comment.author.id)
        )
        self.assertEqual(
            response.json()['data']['author']['username'], comment.author.username
        )
        self.assertEqual(
            response.json()['data']['author']['avatar'], comment.author.avatar
        )
        self.assertEqual(
            response.json()['data']['msg_id'], str(comment.msg.id)
        )
        self.assertEqual(
            response.json()['data']['content'], comment.content
        )
        self.assertEqual(
            response.json()['data']['like'], comment.like
        )
        user_like = models.User.filter(
            id=response.json()['data']['who_like'][0]['user_id']
        )[0]
        self.assertEqual(
            response.json()['data']['who_like'][0]['username'], user_like.username
        )
        self.assertEqual(
            response.json()['data']['who_like'][0]['avatar'], user_like.avatar
        )
        self.assertEqual(
            response.json()['data']['add_date'], comment.add_date.astimezone(
                        timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M:%S")
        )
        self.assertEqual(
            response.json()['data']['mod_date'], comment.mod_date.astimezone(
                        timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M:%S")
        )
        self.assertEqual(
            response.json()['data']['reply_to'], comment.reply_to.id
        )
        self.assertEqual(
            response.json()['data']['parent_comment_id'], comment.parent_comment.id
        )

    def test_get_comments_works_with_wrong_id(self):
        """使用错误id的情况"""
        comment = models.Comment.objects.all()[0]
        request_data = {
            "comment_id": 999999
        }
        response = self.c.get(
            '/ww/comments/', data=request_data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['state']['msg'], 'wrong')

    def test_get_comments_works_with_deleted_id(self):
        """请求已删除评论的情况"""
        comment = models.Comment.objects.all()[0]
        request_data = {
            "comment_id": comment.id
        }
        comment.deleted = 1
        comment.save()
        response = self.c.get(
            '/ww/comments/', data=request_data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['state']['msg'], 'deleted')
        comment.deleted = 0
        comment.save()

    def test_get_comments_works_with_deleted_id(self):
        """请求删除已删除评论的情况"""
        comment = models.Comment.objects.all()[0]
        request_data = {
            "comment_id": comment.id
        }
        comment.deleted = 1
        comment.save()
        response = self.c.get(
            '/ww/comments/', data=request_data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['state']['msg'], 'deleted')
        comment.deleted = 0
        comment.save()


    def test_delete_comment_works_successfully(self):
        """正常删除评论的情况"""
        comment = models.Comment.objects.all()[0]
        request_data = {
            "comment_id": comment.id
        }
        response = self.c.delete(
            '/ww/comments/', data=request_data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['state']['msg'], 'successful')
        self.assertEqual(response.json()['data']
                         ['comment_id'], request_data['comment_id'])
        try:
            with transaction.atomic():
                comment.refresh_from_db()
        except Exception as e:
            print("WTF")
        self.assertEqual(comment.deleted, 1)

    def test_delete_comment_works_with_wrong_id(self):
        """使用错误id删除评论的情况"""
        comment = models.Comment.objects.all()[0]
        request_data = {
            "comment_id": 99999
        }
        response = self.c.delete(
            '/ww/comments/', data=request_data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['state']['msg'], 'wrong')

    def test_give_a_like_to_a_comment_works_successfully(self):
        """正确点赞的情况"""
        comment = models.Comment.objects.filter()[0]
        users_liked = comment.who_like.all()
        users = models.User.objects.all()
        user = list(filter(lambda u: u not in users_liked, users))[0]
        request_data = {
            "comment_id": comment.id,
            "user_id": user.id
        }
        response = self.c.post(
            '/ww/comments/like/', data=request_data, content_type='application/json')
        comment = models.Comment.objects.filter(id=comment.id)[0]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['state']['msg'], 'successful')
        self.assertEqual(response.json()['data']['comment_id'], comment.id)
        self.assertEqual(response.json()['data']['like'], comment.like)
        self.assertIn(user, comment.who_like.all())

    def test_give_two_likes_to_a_comment(self):
        """多次点赞的情况"""
        comment = models.Comment.objects.filter()[0]
        users_liked = comment.who_like.all()
        users = models.User.objects.all()
        user = list(filter(lambda u: u not in users_liked, users))[0]
        request_data = {
            "comment_id": comment.id,
            "user_id": user.id
        }
        response = self.c.post(
            '/ww/comments/like/', data=request_data, content_type='application/json')
        response = self.c.post(
            '/ww/comments/like/', data=request_data, content_type='application/json')
        comment.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['state']['msg'], 'wrong')
        self.assertEqual(response.json()['data']['comment_id'], comment.id)
        self.assertEqual(response.json()['data']['like'], comment.like)
        self.assertIn(user, comment.who_like.all())

    def test_give_a_like_to_a_comment_works_with_wrong_id(self):
        """使用错误id点赞的情况"""
        comment = models.Comment.objects.filter()[0]
        users_liked = comment.who_like.all()
        users = models.User.objects.all()
        user = list(filter(lambda u: u not in users_liked, users))[0]
        request_data = {
            "comment_id": 99999,
            "user_id": 99999
        }
        response = self.c.post(
            '/ww/comments/like/', data=request_data, content_type='application/json')
        comment = models.Comment.objects.filter(id=comment.id)[0]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['state']['msg'], 'wrong')

    def test_give_a_like_to_a_comment_works_with_deleted_id(self):
        """使用已删除id点赞的情况"""
        comment = models.Comment.objects.filter()[0]
        users_liked = comment.who_like.all()
        users = models.User.objects.all()
        user = list(filter(lambda u: u not in users_liked, users))[0]
        user.deleted = 1
        comment.deleted = 1
        user.save()
        comment.save()
        request_data = {
            "comment_id": comment.id,
            "user_id": user.id
        }
        response = self.c.post(
            '/ww/comments/like/', data=request_data, content_type='application/json')
        comment = models.Comment.objects.filter(id=comment.id)[0]
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['state']['msg'], 'deleted')
        user.deleted = 0
        comment.deleted = 0
        user.save()
        comment.save()


class ImagesModelTests(TestCase):
    """
    用于测试Images模块
    """

    c = Client()

    def setUp(self):
        createTestDatabase()

    def test_post_images_works_successfully(self):
        """
        用于测试发送图片是否正常工作
        """
        request_data = {
            "image": '',
            "type": "universal",
        }
        with open('media/pic/rua.jpg', 'rb') as f:
            request_data['image'] = f
            response = self.c.post(
                '/ww/images/', data=request_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['state']['msg'], 'successful')

    def test_get_images_works_successfully(self):
        """
        用于测试获取图片是否工作正常
        """
        request_data = {
            'image_url': 'media/pic/rua.jpg'
        }
        response = self.c.get(
            '/ww/images/', data=request_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'image/jpeg')


class OtherModelTests(TestCase):
    """
    用于测试零散功能
    """

    c = Client()

    def setUp(self):
        createTestDatabase()

    # def test_request_and_testvericode_works_successfully(self):
    #     """
    #     用于测试发送图片是否正常工作
    #     """
    #     phone_number = '13521623093'
    #     request_data = {
    #         "phone_number": phone_number
    #     }
    #     response = self.c.post(
    #         '/ww/request_vericode/', data=request_data, content_type='application/json')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.json()['state']['msg'], 'successful')
    #     request_data = {
    #         "phone_number": '13521623093',
    #         "vericode": cache.get(phone_number)
    #     }
    #     print(request_data['vericode'])
    #     response = self.c.post(
    #         '/ww/test_vericode/', data=request_data, content_type='application/json')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.json()['state']['msg'], 'successful')

    def test_login_works_successfully(self):
        """
        用于测试登陆功能是否正常工作
        """
        user = models.User.objects.all()[0]
        request_data = {
            "phone_number": user.phonenumber,
            "password": user.password
        }
        response = self.c.post(
            '/ww/users/login/', data=request_data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['state']['msg'], 'successful')
        self.assertEqual(response.json()['data']['user_id'], user.id)

    def test_get_static_resources_successfully(self):
        """
        测试获取静态资源是否正常工作
        """
        request_data = {
            'resource_url': 'media/documents/隐私政策.html'
        }
        response = self.c.get('/ww/static_resources/', data=request_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/html')
