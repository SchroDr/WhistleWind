import requests

def testPostInfo():
    data = {
        'userID': '0',
        'content': 'fromPY',
        'x': '0',
        'y': '0',
        'mention': '0',
    }
    """
    files = {'img': [
            open('D://Picture//Pic//Ani//Fate//62536423_p0_master1200.jpg', 'rb'), 
            open('D://Picture//Pic//Ani//Fate//65105861_p0.jpg', 'rb')
            ]}
    """
    files = [
        ('img', open('D://Picture//Pic//Ani//Fate//62536423_p0_master1200.jpg', 'rb')),
        ('img', open('D://Picture//Pic//Ani//Fate//65105861_p0.jpg', 'rb'))
    ]
    
    html = requests.post(url = 'http://localhost:8000/ww/postInfo/', data = data, files = files)
    with open('return.html', 'wb') as f:
        f.write(bytes(html.text, 'utf8'))


testPostInfo()