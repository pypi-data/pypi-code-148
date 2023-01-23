class Joker:
    """
    ###############################
    ######   author: joker   ######
    ######   QQ: 524276169   ######
    ###############################

    findPhonePlace:参数手机号，获取手机号所在地址
    createProgressBar: create a progress bar,
        params:
            max_value[the end value]
            update_value[every epoch update value]
            sleep: whether to set a delay
    sendMessage:send message
        params:
            phone: you know
            message:the message you want send
        notice: remember to change your userid,account and password in the url
    quickAnswer:when you want to attack somebody,you can use this function
        params:
            interval: every interval time send a message
            filename: write the message you want to send into the file,and split it with enter,make sure that every line only have one message
    freeApi: some interesting free api demo
        mode:
            0: every day a sentence
            1: comfort somebody
            2: according to the real time,the function will give a sentence
            3: save a pretty girl video named 1.mp4 in your file root path, no return value
            4: save your qq's headshot
            5: get your qq's nickname
            6: save a scenery video
            7: generate a backup's(tian gou)  quote
            8: generate a real life girl picture
            9: pretty girl video 2.0
            10: save a girl headshot
            11: sadness emotion quote
            12: an interesting conversation
            13: a joke sentence
            14: famous person's quote
            15: get a lover's conversation video
            16: get a hand write picture
            17: get a picture which added some element on your headshot
            18: get a 4K scenery picture
            19: create a picture content your message
                params:msg
    """
    def checkResource(self):
        import os
        if not os.path.exists('resource'):
            os.mkdir('resource')
    def __init__(self):
        self.checkResource()

    def findPhonePlace(self, number=None):
        from phone import Phone
        p = Phone()
        return p.find(number)
        # pip install phone

    def createProgressBar(self, max_value, update_value, sleep=True):
        # pip install progressbar2
        import time
        import progressbar
        p = progressbar.ProgressBar()  # 实例化进度条
        max_value = max_value
        p.start(max_value)
        n = 0
        while n < 100:
            p.update(n)  # 更新
            n += update_value
            if sleep:
                time.sleep(0.1)
        p.finish()

    def sendMessage(self, phone, message):
        import requests
        url = f'http://47.105.48.125:8888/sms.aspx?action=send&userid=541&account=深度学习' \
              f'&password=123456&mobile={phone}&content=【萨维塔的小屋】您的验证码为: {message}（若非本人操作，请删除本短信）'
        resp = requests.post(url)
        print(resp.text)

    def quickAnswer(self, interval=0.5, filename=None):
        import time
        import random
        from pynput.keyboard import Key, Controller
        if filename:
            with open(filename, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            keyboard = Controller()
            choice = random.randint(0, len(lines) - 1)
            command = lines[choice].rstrip()
            keyboard.type(command)
            keyboard.press(Key.enter)
            time.sleep(self.interval)
        else:
            print("you don't select a file")
            return None

    def freeApi(self, mode=0, qq=None,msg=None):
        import os
        import requests
        if mode == 0:
            # a single useless sentence
            resp = requests.get('https://v.api.aa1.cn/api/yiyan/index.php')
            text = resp.text.split('>')[1].split('<')[0]
            return text
        elif mode == 1:
            # when somebody feel sad,you should use this api to comfort him/her
            resp = requests.get('https://v.api.aa1.cn/api/api-wenan-anwei/index.php?type=json')
            text = resp.text.split(":")[1].split('"')[1]
            return text
        elif mode == 2:
            # according to the real time,it will return you different sentences
            resp = requests.get('https://v.api.aa1.cn/api/time-tx/index.php')
            return str(eval(resp.text).get("nxyj"))
        elif mode == 3:
            # save a pretty girl video  (0o0)
            resp = requests.get('https://tucdn.wpon.cn/api-girl/index.php?wpon=json')
            url = 'https://' + eval(resp.text).get("mp4")[4:]
            url = url.split('\\')
            url = '/'.join(url)
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.61'
            }
            'https://tucdn.wpon.cn//api-girl//videos//83.mp4'
            resp = requests.get(url, headers=headers)
            with open('resource/pretty_girl.mp4', 'wb') as f:
                f.write(resp.content)
                print('视频保存完成')
            return 'success'
        elif mode == 4:
            resp = requests.get(f'https://v.api.aa1.cn/api/qqimg/index.php?qq={qq}')
            img_url = resp.text.split('src')[1][1:-1]
            with open('resource/QQ_pic.jpg','wb')as f:
                f.write(requests.get(img_url).content)
                print('获取成功')
            return 'success'
        elif mode == 5:
            resp = requests.get(f'https://v.api.aa1.cn/api/qqnicheng/index.php?qq={qq}')
            nickName = resp.text.split('：')[1].split('<')[0]
            return nickName

        elif mode == 6:
            resp = requests.get('https://v.api.aa1.cn/api/api-fj/index.php?aa1=json')
            num = str(eval(resp.text).get('mp4')).split('.mp4')[0].split('/')[-1]
            video_url = f'https://v.api.aa1.cn/api/api-fj/video/{num}.mp4%20%E5%AE%98%E7%BD%91api.aa1.cn%E5%85%8D%E8%B4%B9%E8%A7%86%E9%A2%91API.mp4'
            with open('resource/scenery.mp4', 'wb') as f:
                f.write(requests.get(video_url).content)
                print('视频保存成功')
            return 'success'
        elif mode == 7:
            resp = requests.get('https://v.api.aa1.cn/api/tiangou/index.php')
            return resp.text.split('>')[1].split("<")[0]
        elif mode == 8:
            resp = requests.get('https://v.api.aa1.cn/api/pc-girl_bz/index.php?wpon=json')
            img_url = 'https:'+eval(resp.text).get('img')
            with open('resource/pretty_girl.jpg', 'wb') as f:
                f.write(requests.get(img_url).content)
                print('图片保存成功')
            return 'success'
        elif mode == 9:
            resp = requests.get('https://v.api.aa1.cn/api/api-dy-girl/index.php?aa1=json')
            video_url ='https:'+eval(resp.text).get('mp4')
            with open('resource/pretty_girl_2.mp4', 'wb') as f:
                f.write(requests.get(video_url).content)
                print('视频保存成功')
            return 'success'
        elif mode == 10:
            resp = requests.get('https://v.api.aa1.cn/api/api-tx/index.php?wpon=json')
            img_url = 'https:'+eval(resp.text).get('img')
            with open('resource/head_shot_girl.jpg','wb')as f:
                f.write(requests.get(img_url).content)
                print('图片保存成功')
            return 'success'
        elif mode == 11:
            resp = requests.get('https://v.api.aa1.cn/api/api-wenan-qg/index.php?aa1=json')
            return eval(resp.text)[0].get('qinggan')
        elif mode == 12:
            resp = requests.get('https://v.api.aa1.cn/api/api-wenan-shenhuifu/index.php?aa1=json')
            return eval(resp.text)[0].get("shenhuifu")
        elif mode == 13:
            resp = requests.get('https://v.api.aa1.cn/api/api-wenan-gaoxiao/index.php?aa1=json')
            return eval(resp.text)[0].get('gaoxiao')
        elif mode == 14:
            resp = requests.get('https://v.api.aa1.cn/api/api-wenan-mingrenmingyan/index.php?aa1=json')
            return eval(resp.text)[0].get('mingrenmingyan')
        elif mode == 15:
            resp = requests.get('https://v.api.aa1.cn/api/api-video-qinglvduihua/index.php?aa1=json')
            video_url = 'https:'+eval(resp.text).get('mp4')
            with open('resource/conversation.mp4','wb')as f:
                f.write(requests.get(video_url).content)
            return 'success'
        elif mode == 16:
            resp = requests.get('https://v.api.aa1.cn/api/api-gqsh/index.php?wpon=json')
            img_url = 'https:'+eval(resp.text).get('img')
            with open('resource/handwrite.jpg','wb')as f:
                f.write(requests.get(img_url).content)
            return 'success'
        elif mode == 17:
            resp = requests.get(f'https://v.api.aa1.cn/api/api-tksc/sc.php?qq={qq}')
            with open('resource/headshot_festival.jpg','wb')as f:
                f.write(resp.content)
            return 'success'
        elif mode == 18:
            resp = requests.get('https://v.api.aa1.cn/api/api-fj-1/index.php?aa1=yuantu')
            with open('resource/scenery_4k.jpg','wb')as f:
                f.write(resp.content)
            return 'success'
        elif mode==19:
            resp = requests.get(f'https://v.api.aa1.cn/api/api-jupai/index.php?msg={msg}')
            with open('resource/little_people.jpg','wb')as f:
                f.write(resp.content)
            return 'success'
if __name__ == '__main__':
    joker = Joker()
    # joker.findPhonePlace(15383312439)
    # joker.createProgressBar(100,1)
    # joker.sendMessage(15383312439, 'hello')
    # joker.quickAnswer(0.5)
    # result = joker.freeApi(mode=16,qq=524276169)
    # result = joker.freeApi(mode=17,qq=524276169)
    # result = joker.freeApi(mode=18,qq=524276169)
    result = joker.freeApi(mode=19,qq=524276169,msg='你大爷')
    # result = joker.freeApi(mode=20,qq=524276169)
    # result = joker.freeApi(mode=21,qq=524276169)
    print(result)
    # print(joker.__doc__)
