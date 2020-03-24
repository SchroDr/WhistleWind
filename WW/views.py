"""
    本模块遵循Restful原则，使用不同的HTTP动词对应不同类型的操作
    POST: 增加
    GET: 获取
    PUT: 修改
    DELETE: 删除
    接口的具体功能见
    http://rap2.taobao.org/organization/repository/editor?id=224734&mod=313234
"""

import exrex
import json
import os
import demjson
import traceback
from . import models, sendEmail
from django.views import View
from django.http import JsonResponse, FileResponse, QueryDict
from django.views.decorators.http import require_GET, require_http_methods, require_POST
from django.core.cache import cache
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname('__file__')))
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
PIC_ROOT = os.path.join(MEDIA_ROOT, 'pic')

# jhc work----------------------------------------------------------------


class UsersView(View):
    """
    本模块用于对用户信息进行增删改查
    """

    def post(self, request):
        # TO DO 用户注册
        result = {
            "state": {
                "msg": "existed",
                'descripntion': 'Null',
            },
        }
        try:
            post = demjson.decode(request.body)
            phone_number = post["phone_number"]
            password = post["password"]
            # veri_code = request.POST.get("veri_code")
            user = models.User.objects.filter(phonenumber=phone_number)
            if len(user) == 1:  # 已存在
                result['state']['msg'] = 'existed'
                return JsonResponse(result)
            elif len(user) == 0:  # 不存在，可以创建
                user = models.User.objects.create(
                    phonenumber=phone_number, password=password)
                user_id = user.id
                result['data'] = {'user_id': user_id}
                result['state']['msg'] = 'successful'
                return JsonResponse(result)
        except Exception as e:
            result['state']['msg'] = 'failed'
            result['state']['description'] = str(repr(e))
            print('\nrepr(e):\t', repr(e))
            print('traceback.print_exc():', traceback.print_exc())
            return JsonResponse(result)

    def get(self, request):
        # TO DO 获取用户信息
        # default_number = 10  # 没有请求数据默认返回数量
        result = {
            "data": {
                "user_id": 0,
                "username": "",
                "email": "",
                "phonenumber": "",
                "avatar": "",
                "introduction": "",
                "follows_number": 0,
                "followers_number": 0,
                "messages_number": 0,
                "comments_number": 0,
                "follows": [],
                "followers": [],
                "messages": [],
                "comments": [],
            },
            "state": {
                'msg': 'failed',
                'descripntion': 'Null',
            }
        }
        try:
            user_id = request.GET.get('user_id')
            follows_start = int(request.GET.get('follows_start'))
            follows_number = int(request.GET.get('follows_number'))
            followers_start = int(request.GET.get('followers_start'))
            followers_number = int(request.GET.get('followers_number'))
            messages_start = int(request.GET.get('messages_start'))
            messages_number = int(request.GET.get('messages_number'))
            comments_start = int(request.GET.get('comments_start'))
            comments_number = int(request.GET.get('comments_number'))
            # -----------------------------------------------------
            userInfo = models.User.objects.filter(id=user_id)
            userInfo = userInfo.first()
            result['data']['user_id'] = int(user_id)
            result['data']['username'] = userInfo.username
            result['data']['email'] = userInfo.email
            result['data']['phonenumber'] = userInfo.phonenumber
            result['data']['avatar'] = str(userInfo.avatar)
            result['data']['introduction'] = userInfo.introduction
            '''
            关注的人
            '''
            follows = models.Followship.objects.filter(
                fan=user_id).order_by('date')
            allFollows = len(follows)
            result['data']['follows_number'] = allFollows
            res = self.request_return_user(
                follows, follows_start, follows_number)
            for i in res:
                oneFoll = models.User.objects.get(id=str(i.followed_user))
                result['data']['follows'].append(
                    {
                        "user_id": str(i.followed_user),
                        "username": oneFoll.username,
                        "avatar": str(oneFoll.avatar)
                    }
                )
            '''
            粉丝
            '''
            followers = models.Followship.objects.filter(
                followed_user=user_id).order_by('date')
            allFollowers = len(followers)
            result['data']['followers_number'] = allFollowers
            res = self.request_return_user(
                followers, followers_start, followers_number)
            for i in res:
                oneFoll = models.User.objects.get(id=str(i.fan))
                result['data']['followers'].append(
                    {
                        "user_id": str(i.fan),
                        "username": oneFoll.username,
                        "avatar": str(oneFoll.avatar)
                    }
                )
            '''
            信息
            '''
            messages = models.Message.objects.filter(
                author=user_id).order_by('-add_date')
            allMessages = len(messages)
            result['data']['messages_number'] = allMessages
            res = self.request_return_user(
                messages, messages_start, messages_number)
            for i in res:
                result['data']['messages'].append(
                    {
                        "message_id": str(i.id),
                        "title": i.title,
                        "content": i.content
                    }
                )
            '''
            评论
            '''
            comments = models.Comment.objects.filter(
                author=user_id).order_by('-add_date')
            allComments = len(comments)
            result['data']['comments_number'] = allComments
            res = self.request_return_user(
                comments, comments_start, comments_number)
            for i in res:
                result['data']['comments'].append(
                    {
                        "comment_id": str(i.id),
                        "content": i.content
                    }
                )
            result['state']['msg'] = 'successful'
        except Exception as e:
            result['state']['msg'] = 'failed'
            result['state']['descripntion'] = repr(e)
            del result['data']
            print('\nrepr(e):\t', repr(e))
            print('traceback.print_exc():', traceback.print_exc())
        return JsonResponse(result)

    def request_return_user(self, allContent, start, num):
        res = allContent
        # 返回全部
        if num == -1:
            res = res
        # 开始位置大于总数
        elif start > len(res) - 1:
            # 总数小于11，返回全部
            if len(res) <= 10:
                res = res
            # 总数较多，返回10条
            else:
                res = res[0:10]
        # 开始位置+请求数量=超出总数
        elif start <= len(res) - 1 and (start+num) > len(res)-1:
            res = res[start:]
        else:
            res = res[start:start+num]
        return res

    def put(self, request):
        # TO DO 修改用户信息
        result = {
            "state": {
                "msg": "successful",
                'descripntion': 'Null',
            },
            "data": {
                "user_id": 0
            }
        }
        try:
            put = demjson.decode(request.body)
            user_id = put['user_id']
            # username = put['username']
            # email = put['email']
            # phonenumber = put['phonenumber']
            # avatar = put['avatar']
            # introduction = put['introduction']
            user = models.User.objects.filter(id=user_id).first()
            if user != None:
                # try:
                if 'username' in put:
                    user.username = put['username']
                if 'email' in put:
                    user.email = put['email']
                if 'phonenumber' in put:
                    user.phonenumber = put['phonenumber']
                if 'avatar' in put:
                    user.avatar = put['avatar']
                if 'introduction' in put:
                    user.introduction = put['introduction']
                user.save()
                result['state']['msg'] = 'successful'
                result['data']['user_id'] = user_id
                # except:
                #     result['state']['msg'] = 'failed'
            else:
                result['state']['msg'] = 'failed'
        except Exception as e:
            result['state']['msg'] = 'failed'
            result['state']['description'] = str(repr(e))
            print('\nrepr(e):\t', repr(e))
            print('traceback.print_exc():', traceback.print_exc())
        return JsonResponse(result)

    def delete(self, request):
        # TO DO 删除用户信息
        # 暂无需实现,保留接口，暂不实现此功能
        pass
# jhc work----------------------------------------------------------------


"""
    Message模块由SchroDr绝赞摸鱼中
"""


class MessagesView(View):
    """
    本模块用于对消息进行增删改查
    """

    def post(self, request):
        # TO DO 发送消息
        result = {
            "state": {
                "msg": "successful",
                "description": ""
            },
            "data": {
                "msg_id": 0
            }
        }
        try:
            request_data = demjson.decode(request.body)
            author_id = request_data['user_id']
            pos_x = request_data['position']['pos_x']
            pos_y = request_data['position']['pos_y']
            title = request_data['title']
            content = request_data['content']
            images = request_data['images']
            author = models.User.objects.filter(id=author_id)[0]
            message = models.Message.objects.create(
                pos_x=pos_x,
                pos_y=pos_y,
                title=title,
                content=content,
                author=author
            )
            message.save()
            for image in images:
                messageImage = models.MessageImage.objects.create(
                    message=message, img=image['image_url']
                )
                messageImage.save()
            result['state']['msg'] = 'successful'
            result['data']['msg_id'] = message.id
            return JsonResponse(result)
        except Exception as e:
            result['state']['msg'] = 'failed'
            result['state']['description'] = str(repr(e))
            result.pop('data')
            print('\nrepr(e):\t', repr(e))
            print('traceback.print_exc():', traceback.print_exc())
            return JsonResponse(result)

    def get(self, request):
        # TO DO 获取消息
        result = {
            "data": {
                'msg_id': 0,
                "position": {
                    "pos_x": 0,
                    "pos_y": 0
                },
                "title": "",
                "content": "",
                "author": {
                    "author_id": 0,
                    "username": "",
                    "avatar": ""
                },
                "like": 0,
                "dislike": 0,
                "who_like": [
                ],
                "who_dislike": [
                ],
                "add_date": "",
                "mod_date": "",
                "comments": [
                ],
                "images": [

                ]
            },
            "state": {
                "msg": "",
                "description": ""
            }
        }
        try:
            # request_data = demjson.decode(request.body)
            request_data = request.GET.dict()
            msg_id = request_data['msg_id']
            message = models.Message.objects.filter(id=msg_id)[0]
            author = message.author
            result['data']['msg_id'] = message.id
            result['data']['position']['pos_x'] = message.pos_x
            result['data']['position']['pos_y'] = message.pos_y
            result['data']['title'] = message.title
            result['data']['content'] = message.content
            result['data']['author']['author_id'] = author.id
            result['data']['author']['username'] = author.username
            result['data']['author']['avatar'] = author.avatar
            result['data']['like'] = message.like
            result['data']['dislike'] = message.dislike
            for i, user in enumerate(message.who_like.all()):
                user_info = {
                    "user_id": user.id,
                    "username": user.username,
                    "avatar": user.avatar.path
                }
                result['data']['who_like'].append(user_info)
                if i >= 9:
                    break
            for i, user in enumerate(message.who_dislike.all()):
                user_info = {
                    "user_id": user.id,
                    "username": user.username,
                    "avatar": user.avatar.path
                }
                result['data']['who_dislike'].append(user_info)
                if i >= 9:
                    break
            result['add_data'] = message.add_date
            result['mod_date'] = message.mod_date
            for i, comment in enumerate(message.comment_set.all()):
                comment_info = {
                    "comment_id": comment.id,
                    "content": comment.content,
                    'like': comment.like,
                    'author': {
                        'author_id': comment.author.id,
                        'username': comment.author.username,
                        'avatar': comment.author.username
                    }
                }
                result['data']['comments'].append(comment_info)
                if i >= 9:
                    break
            for i, image in enumerate(message.messageimage_set.all()):
                message_info = {
                    'image_url': image.img
                }
                result['data']['images'].append(message_info)
            result['state']['msg'] = 'successful'
            return JsonResponse(result)
        except Exception as e:
            result['state']['msg'] = 'failed'
            result['state']['description'] = str(repr(e))
            result.pop('data')
            print('\nrepr(e):\t', repr(e))
            print('traceback.print_exc():', traceback.print_exc())
            return JsonResponse(result)

    def put(self, request):
        # TO DO 修改消息
        result = {
            "state": {
                "msg": "",
                "description": ""
            },
            "data": {
                "msg_id": 0
            }
        }
        try:
            request_data = demjson.decode(request.body)
            msg_id = request_data['msg_id']
            message = models.Message.objects.filter(id=msg_id)[0]
            if 'title' in request_data.keys():
                message.title = request_data['title']
            if 'content' in request_data.keys():
                message.content = request_data['content']
            if 'images' in request_data.keys():
                message.messageimage_set.all().delete()
                for image in request_data['images']:
                    message_image = models.MessageImage.objects.create(
                        img=image['image_url'],
                        message=message
                    )
                    message_image.save()
            message.save()
            result['state']['msg'] = 'successful'
            result['data']['msg_id'] = message.id
            return JsonResponse(result)
        except Exception as e:
            result['state']['msg'] = 'failed'
            result['state']['description'] = str(repr(e))
            result.pop('data')
            print('\nrepr(e):\t', repr(e))
            print('traceback.print_exc():', traceback.print_exc())
            return JsonResponse(result)

    def delete(self, request):
        # TO DO 删除消息
        result = {
            "state": {
                "msg": "",
                "description": ""
            },
            "data": {
                "msg_id": 0
            }
        }
        try:
            request_data = demjson.decode(request.body)
            msg_id = request_data['msg_id']
            message = models.Message.objects.filter(id=msg_id)[0]
            message.delete()
            result['state']['msg'] = 'successful'
            result['data']['msg_id'] = msg_id
            return JsonResponse(result)
        except Exception as e:
            result['state']['msg'] = 'failed'
            result['state']['description'] = str(repr(e))
            result.pop('data')
            print('\nrepr(e):\t', repr(e))
            print('traceback.print_exc():', traceback.print_exc())
            return JsonResponse(result)


# jhc----------------
class CommentsView(View):
    """
    本模块用于对评论进行增删改查；
    """

    def post(self, request):
        # TO DO 发送评论
        result = {
            "state": {
                "msg": "successful"
            },
            "data": {
                "comment_id": 0
            }
        }
        comment = demjson.decode(request.body)
        # print(comment)
        # user_id = request.POST.get("user_id")
        # content = request.POST.get("content")
        # msg_id = request.POST.get("msg_id")
        # print(user_id, msg_id)
        try:
            user = models.User.objects.filter(id=comment['user_id'])[0]
            mess = models.Message.objects.filter(id=comment['msg_id'])[0]
            comm = models.Comment.objects.create(
                msg=mess,
                content=comment['content'],
                author=user)
            comm.save()
            result['state']['msg'] = 'successful'
            result['data']['comment_id'] = comm.id
        except:
            result['state']['msg'] = 'failed'
        return JsonResponse(result)

    def get(self, request):
        # TO DO 获取评论
        result = {
            "data": {
                "comment_id": 0,
                "msg_id": 0,
                "author": {
                    "author_id": "",
                    "username": "",
                    "avatar": ""
                },
                "content": "",
                "like": 0,
                "who_like": [
                    {
                        "user_id": 0,
                        "username": "",
                        "avatar": ""
                    }
                ],
                "add_date": "",
                "mod_date": ""
            },
            "state": {
                "msg": "failed"
            }
        }

        comment_id = request.GET.get('comment_id')
        try:
            comment = models.Comment.objects.filter(id=comment_id)
            if len(comment) != 0:
                comment = comment.first()
                if comment.deleted != 1:
                    result['data']['comment_id'] = comment.id
                    result['data']['msg_id'] = str(comment.msg)
                    result['data']['author']['author_id'] = str(comment.author)
                    result['data']['author']['username'] = str(comment.author.username)
                    result['data']['author']['avatar'] = str(comment.author.avatar)
                    result['data']['content'] = comment.content
                    result['data']['like'] = comment.like
                    result['data']['add_date'] = str(comment.add_date)
                    result['data']['mod_date'] = str(comment.mod_date)
                    who_like = comment.who_like.all()
                    for i in who_like:
                        oneLike = {
                            "user_id": i.id,
                            "username": i.username,
                            "avatar": i.avatar,
                        }
                        result['who_like'].append(oneLike)
                    result['state']['msg'] = 'successful'
        except:
            pass
        result = demjson.decode(str(result))
        # result = json.
        return JsonResponse(result)

    def put(self, request):
        # TO DO 修改评论
        pass

    def delete(self, request):
        # TO DO 删除评论
        result = {
            "state": {
                "msg": "successful"
            },
            "data": {
                "comment_id": 0
            }
        }
        delete = demjson.decode(request.body)
        try:
            comm = models.Comment.objects.get(id=delete['comment_id'])
            if comm.deleted != 1:
                comm.deleted = 1
                comm.save()
                result['state']['msg'] = 'successful'
                result['data']['comment_id'] = comm.id
        except:
            result['state']['msg'] = 'failed'
        return JsonResponse(result)
# jhc-----------------------------------


"""
Image模块由SchroDr绝赞划水中！
"""


class ImagesView(View):
    """
    本模块用于上传下载图片
    """

    def post(self, request):
        # TO DO 上传图片
        result = {
            "data": {
                "image_url": "",
                "description": ""
            },
            "state": {
                "msg": ""
            }
        }
        try:
            image_file = request.FILES.get("image")
            image_type = request.POST.get("type")
            image = models.Image.objects.create(
                img=image_file,
                type=image_type
            )
            image.save()
            result['data']['image_url'] = image.img.url
            result['state']['msg'] = 'successful'
            return JsonResponse(result)
        except Exception as e:
            result['state']['msg'] = 'failed'
            result['state']['description'] = str(repr(e))
            result.pop('data')
            print('\nrepr(e):\t', repr(e))
            print('traceback.print_exc():', traceback.print_exc())
            return JsonResponse(result)

    def get(self, request):
        # TO DO 返回图片
        try:
            url = request.GET.get('image_url')
            url = os.path.join(PROJECT_ROOT, url)
            return FileResponse(open(url, 'rb'))
        except Exception as e:
            result = {
                "state": {
                    "msg": "",
                    "description": ""
                }
            }
            result['state']['msg'] = 'failed'
            result['state']['description'] = str(repr(e))
            print('\nrepr(e):\t', repr(e))
            print('traceback.print_exc():', traceback.print_exc())
            return JsonResponse(result)


def login(request):
    # TO DO 登陆
    result = {
        "state": {
            "msg": "",
            "description": ""
        },
        "data": {
            "cookie": "",
            "user_id": 0
        }
    }
    try:
        request_data = demjson.decode(request.body)
        phone_number = request_data['phone_number']
        password = request_data['password']
        user = models.User.objects.filter(phonenumber=phone_number)[0]
        if user.password == password:
            result['state']['msg'] = 'successful'
            result['data']['user_id'] = user.id
            return JsonResponse(result)
        else:
            result['state']['msg'] = 'wrong'
            return JsonResponse(result)
    except IndexError as e:
        result['state']['msg'] = 'nonexistent'
        result['state']['description'] = str(repr(e))
        result.pop('data')
        print('\nrepr(e):\t', repr(e))
        print('traceback.print_exc():', traceback.print_exc())
        return JsonResponse(result)
    except Exception as e:
        result['state']['msg'] = 'failed'
        result['state']['description'] = str(repr(e))
        result.pop('data')
        print('\nrepr(e):\t', repr(e))
        print('traceback.print_exc():', traceback.print_exc())
        return JsonResponse(result)


def requestVericode(request):
    # TO DO 向用户手机发送验证码，并将验证码存入数据库中
    result = {
        "state": {
            "msg": "",
            "description": ""
        },
        "data": {
            "time_limit": ''
        }
    }
    time_limit = 300
    try:
        request_data = demjson.decode(request.body)
        phone_number = request_data['phone_number']

        client = AcsClient('LTAIFp0FVf7njxtN',
                           'TJ1NBIx8RqJhqzuMgC0KtXUzYCxZDw', 'cn-hangzhou')
        request = CommonRequest()
        request.set_accept_format('json')
        request.set_domain('dysmsapi.aliyuncs.com')
        request.set_method('POST')
        request.set_protocol_type('https')  # https | http
        request.set_version('2017-05-25')
        request.set_action_name('SendSms')

        request.add_query_param('RegionId', "cn-hangzhou")
        request.add_query_param('PhoneNumbers', phone_number)
        request.add_query_param('SignName', "顺呼验证码")
        request.add_query_param('TemplateCode', "SMS_158051516")
        code = exrex.getone(r"\d{6}")
        request.add_query_param('TemplateParam', "{'code': '%s'}" % code)

        response = client.do_action(request)
        # print(str(response, encoding = 'utf-8'))
        cache.set(phone_number, code, time_limit)
        result['state']['msg'] = 'successful'
        result['data']['time_limit'] = time_limit
        return JsonResponse(result)
    except Exception as e:
        result.pop('data')
        result['state']['description'] = str(repr(e))
        result['state']['msg'] = 'failed'
        print('\nrepr(e):\t', repr(e))
        print('traceback.print_exc():', traceback.print_exc())
        return JsonResponse(result)


def testVericode(request):
    # TO DO 验证验证码是否正确
    result = {
        "state": {
            "msg": "",
            "description": ""
        }
    }
    try:
        request_data = demjson.decode(request.body)
        phone_number = request_data['phone_number']
        vericode = request_data['vericode']
        if vericode == cache.get(phone_number):
            result['state']['msg'] = 'successful'
            return JsonResponse(result)
        else:
            result['state']['msg'] = 'wrong'
            return JsonResponse(result)
    except Exception as e:
        result['state']['msg'] = 'failed'
        result['state']['description'] = str(repr(e))
        print('\nrepr(e):\t', repr(e))
        print('traceback.print_exc():', traceback.print_exc())
        return JsonResponse(result)


def messagesSet(request):
    # TO DO 根据地理信息等返回一组消息
    result = {
        "state": {
            "msg": "",
            "description": ""
        },
        "data": {
            "messages": [
            ]
        }
    }
    try:
        request_data = request.GET.dict()
        user_id = request_data['user_id']
        pos_x = float(request_data['pos_x'])
        pos_y = float(request_data['pos_y'])
        width = float(request_data['width'])
        height = float(request_data['height'])
        number = int(request_data['number'])

        messages = models.Message.objects.filter(
            pos_x__gte=pos_x-width/2, pos_x__lte=pos_x+width/2,
            pos_y__gte=pos_y-height/2, pos_y__lte=pos_y+height/2)

        for i, message in enumerate(messages):
            if i >= number:
                break
            message_info = {
                "msg_id": message.id,
                "title": message.title,
                "content": message.content,
                "images": [
                ],
                "author": {
                    "author_id": message.author.id,
                    "username": message.author.username,
                    "avatar": message.author.avatar
                },
                "position": {
                    "pos_x": message.pos_y,
                    "pos_y": message.pos_x
                }
            }
            if len(message.messageimage_set.all()) > 0:
                message_info['images'].append({
                    "image_url": message.messageimage_set.all()[0].img
                })
            result['data']['messages'].append(message_info)
        result['state']['msg'] = 'successful'
        return JsonResponse(result)
    except Exception as e:
        result['state']['msg'] = 'failed'
        result['state']['description'] = str(repr(e))
        result.pop('data')
        print('\nrepr(e):\t', repr(e))
        print('traceback.print_exc():', traceback.print_exc())
        return JsonResponse(result)


def messagesLike(request):
    # TO DO 给消息点赞
    result = {
        "state": {
            "msg": "",
            "description": ""
        },
        "data": {
            "msg_id": 0,
            "like": 0,
            "dislike": 0
        }
    }
    try:
        request_data = demjson.decode(request.body)
        msg_id = request_data['msg_id']
        user_id = request_data['user_id']
        message = models.Message.objects.filter(id=msg_id)[0]
        user = models.User.objects.filter(id=user_id)[0]
        if user in message.who_like.all():
            result['state']['msg'] = 'wrong'
            result['state']['description'] = "Liked once"
        else:
            message.like += 1
            message.who_like.add(user)
            message.save()
            result['state']['msg'] = 'successful'
        result['data']['msg_id'] = message.id
        result['data']['like'] = message.like
        result['data']['dislike'] = message.dislike
        return JsonResponse(result)
    except Exception as e:
        result.pop('data')
        result['state']['msg'] = 'failed'
        result['state']['description'] = str(repr(e))
        print('\nrepr(e):\t', repr(e))
        print('traceback.print_exc():', traceback.print_exc())
        return JsonResponse(result)


def messagesDislike(request):
    # TO DO 给消息点踩
    result = {
        "state": {
            "msg": "",
            "description": ""
        },
        "data": {
            "msg_id": 0,
            "like": 0,
            "dislike": 0
        }
    }
    try:
        request_data = demjson.decode(request.body)
        msg_id = request_data['msg_id']
        user_id = request_data['user_id']
        message = models.Message.objects.filter(id=msg_id)[0]
        user = models.User.objects.filter(id=user_id)[0]
        if user in message.who_dislike.all():
            result['state']['msg'] = 'wrong'
            result['state']['description'] = "Disliked once"
        else:
            message.dislike += 1
            message.who_dislike.add(user)
            message.save()
            result['state']['msg'] = 'successful'
        result['data']['msg_id'] = message.id
        result['data']['like'] = message.like
        result['data']['dislike'] = message.dislike
        return JsonResponse(result)
    except Exception as e:
        result.pop('data')
        result['state']['msg'] = 'failed'
        result['state']['description'] = str(repr(e))
        print('\nrepr(e):\t', repr(e))
        print('traceback.print_exc():', traceback.print_exc())
        return JsonResponse(result)


def messagesMentioned(request):
    # TO DO 查看被@的信息
    pass


def commentsLike(request):
    # TO DO 给评论点赞
    result = {
        "state": {
            "msg": "",
            "description": ""
        },
        "data": {
            "comment_id": 0,
            "like": 0,
        }
    }
    try:
        request_data = demjson.decode(request.body)
        msg_id = request_data['comment_id']
        user_id = request_data['user_id']
        comment = models.Comment.objects.filter(id=msg_id)[0]
        user = models.User.objects.filter(id=user_id)[0]
        if user in comment.who_like.all():
            result['state']['msg'] = 'wrong'
            result['state']['description'] = "Liked once"
        else:
            comment.like += 1
            comment.who_like.add(user)
            comment.save()
            result['state']['msg'] = 'successful'
        result['data']['comment_id'] = comment.id
        result['data']['like'] = comment.like
        return JsonResponse(result)
    except Exception as e:
        result.pop('data')
        result['state']['msg'] = 'failed'
        result['state']['description'] = str(repr(e))
        print('\nrepr(e):\t', repr(e))
        print('traceback.print_exc():', traceback.print_exc())
        return JsonResponse(result)


def staticResources(request):
    # TO DO 获取静态资源
    try:
        url = request.GET.get('resource_url')
        url = os.path.join(PROJECT_ROOT, url)
        return FileResponse(open(url, 'rb'))
    except Exception as e:
        result = {
            "state": {
                "msg": "",
                "description": ""
            }
        }
        result['state']['msg'] = 'failed'
        result['state']['description'] = str(repr(e))
        print('\nrepr(e):\t', repr(e))
        print('traceback.print_exc():', traceback.print_exc())
        return JsonResponse(result)
