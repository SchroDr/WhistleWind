

1.登录//接口：lastation.me:8000/ww/login/
请求方式:post
请求目标:
请求参数:
email
password
返回格式:
{
isSucceed: (0或1)			//登录成功
isNotExist:(0或1)			//用户不存在
isWrong:	(0或1)			//账号或密码错误不存在
userId:
}



2.注册//接口：lastation.me:8000/ww/register/
请求方式:post
请求目标:
请求参数:
password
email//邮箱
返回格式:
{
isSucceed: (0或1)			//注册成功
isExist:(0或1)				//用户已存在
}

3.获取信息//接口：lastation.me:8000/ww/getMessages/
请求方式:post
请求目标:
请求参数:
x:			//地图中心点的横坐标
y:			//地图中心点的横坐标
zoom:		//地图缩放级别
width://经度
height://纬度度
返回格式:
{
msg:{
title://信息标题
content://信息内容
img:{
//图片url
}//可能有多个图片
msgId://每条信息有自己的id
x://信息的横坐标
y://信息的纵坐标
}//一个信息一条
}

4.打开信息详情//接口：lastation.me:8000/ww/getMsgInfo/
请求方式:post
请求目标:
请求参数:
msgId
返回格式:
{
name://作者用户名
userID:
headerImgUrl://作者头像
like://点赞数
dislike://点踩数
follow://转发数
time://信息发送时间
commentsId:{}
}





4.打开评论//接口：lastation.me:8000/ww/getComtInfo/
请求方式:post
请求目标:
请求参数:
commentsId
返回格式:
{
name://评论用户名
headerImgUrl://评论者头像
time://评论时间
content://评论内容
imgUrl://评论中只允许放一张图片
like://评论的点赞数量

}


5.点赞//接口：lastation.me:8000/ww/giveALIke/
请求方式:post
请求目标:
请求参数:
msgId
userId
返回格式:无

5.点踩//接口：lastation.me:8000/ww/giveDisALIke/
请求方式:post
请求目标:
请求参数:
msgId
userId
返回格式:无

5.转发
请求方式:post
请求目标:
请求参数:
msgId 
userID
x:
y:
返回格式:
{
isSucceed:
}

6.发表评论//接口：lastation.me:8000/ww/postComt/


请求方式:post
请求目标:
请求参数:
msgId 
userID
content
img
返回格式:
{
isSucceed:
}

7.发布信息//接口：lastation.me:8000/ww/postInfo/
请求方式:post
请求目标:
请求参数: 
userID
content
title:
img:{
}//格式类型是file
x
y
mention://被@了的好友id
返回格式:
{
isSucceed:
}

7.打开用户详情页
请求方式:post
请求目标:
请求参数: 
userID://被打开的用户的id
返回格式:
{
name:
summary://用户简介
headerImg:
isFollowed://是否已关注
msg:{
time:
content:
img:{}
}//先获取(若干条)过往信息
}

7.获取通知(现阶段主要是看有没有被@)
请求方式:post,每2分钟请求一次
请求目标:
请求参数: 
userID://被打开的用户的id
返回格式:
{
msgId://被哪条信息@了
}

8.关注
请求方式:post
请求目标:
请求参数: 
userID://用户的id
targetUserId://被取消关注的用户的id
返回格式:
{
isSucceed:
}

9.取消关注
请求方式:post
请求目标:
请求参数: 
userID://用户的id
targetUserId://被取消关注的用户的id
返回格式:
{
isSucceed:
}

10.获取好友列表
请求方式:post
请求目标:
请求参数: 
userID://用户的id
返回格式:
{
{
name
useId
summary://简介
}
}

11.设置头像
请求方式:post
请求目标:
请求参数: 
userID://用户的id
headerImg://file文件格式
返回格式:
{
isSucceed:
}
11.设置简介
请求方式:post
请求目标:
请求参数: 
userId:
summary:
返回格式:
{
isSucceed:
}
12.评论点赞
请求方式:post
请求目标:
请求参数: 
commentId
userId
返回格式:
{
isSucceed:
}

13.获取图片//接口：lastation.me:8000/ww/getPic/
请求方式:post
请求目标:
请求参数: 
Image_url
返回格式:
图片






















