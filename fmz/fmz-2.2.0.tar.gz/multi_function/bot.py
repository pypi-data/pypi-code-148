from requests import post, get
import os

directory = (os.path.split(os.path.realpath(__file__))[0]).split("\\")
directory = "/".join(directory)+"/"

def chat(text: set):
    # try:
        headers = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36 Edg/103.0.1264.77"
        }
        url = "https://www.yuanfudao.com/ada-student-app-api/api/yuanbot"
        url1 = "https://www.yuanfudao.com/ada-student-app-api/api/speech/audio-to-text"
        r = post(url=url, data={"question": text}, headers=headers)
        answer = r.json()["answer"]
        r = get(url=answer, headers=headers)
        f = open(directory+"1.wav", "wb")
        f.write(r.content)
        f.close()
        r = post(url=url1, files={"voice": open(directory+"1.wav", "rb")}, headers=headers)
        os.remove(directory+"1.wav")
        return r.json()["text"]
    # except:
    #     return False