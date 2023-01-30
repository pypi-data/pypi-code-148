"""
内置库
"""
import os
import shutil
import urllib.parse
from concurrent.futures import ThreadPoolExecutor

"""
三方库：
	requests
	pycryptodome
"""
import requests
from Crypto.Cipher import AES


# 获取第二个m3u8
def step0(str0, url):
    url_info = urllib.parse.urlsplit(url)
    url = url_info.scheme + "://" + url_info.netloc
    list0 = str0.split("\n")
    for index, value in enumerate(list0):
        if value.startswith("#EXT-X-STREAM-INF"):
            return requests.get(url + list0[index + 1]).text
    return str0


# 解析m3u8
def step1(str0):
    method0 = None
    key0 = None
    list0 = []
    # 加密信息
    if str0.__contains__("#EXT-X-KEY"):
        for item in str0.split("\n"):
            if item.startswith("#EXT-X-KEY"):
                method0 = item[item.index("METHOD=") + 7:item.index(",URI")]
                key0 = requests.get(item[item.index("\"") + 1: item.rindex("\"")]).text
                break
    print("解析（3/4）")
    # ts文件列表
    for item in str0.split("\n"):
        if item.startswith("http"):
            list0.append(item)
    print("解析（4/4）")
    return {
        "method": method0,
        "key": key0,
        "list": list0
    }


# 创建缓存文件夹
def rebuildTemp(str0):
    if os.path.exists(str0):
        shutil.rmtree(str0)
    os.mkdir(str0)


# 一个下载任务
def downOne(index, url, key, temp):
    if key is None:
        data = requests.get(url).content
        file = open(f"./{temp}/{index}.ts", "wb")
        file.write(data)
        file.close()
        print(f'[{index}]', end="")
    else:
        data = requests.get(url).iter_content(chunk_size=1024)
        key0 = bytes(key, 'utf8')
        file = open(f"./{temp}/{index}.ts", "wb")
        cryptor = AES.new(key0, AES.MODE_CBC, key0)
        for chunk in data:
            if chunk:
                file.write(cryptor.decrypt(chunk))
        file.close()
        print(f'[{index}]', end="")


# 线程池批量下载
def downAll(list0, key, temp, size):
    pool = ThreadPoolExecutor(max_workers=size)
    for index, value in enumerate(list0):
        pool.submit(downOne, index, value, key, temp)
    pool.shutdown(wait=True)


# 准备合并
def step2(size, temp):
    file = open(f"{temp}/info.txt", "w")
    index = 0
    while index < size:
        file.write(f"file '{index}.ts'\n")
        index = index + 1
    file.close()


# 进行合并
def step3(temp, filename):
    os.system(f"ffmpeg -f concat -safe 0 -i {temp}/info.txt -c copy {filename}.mp4")


# 删除缓存文件夹
def removeTemp(str0):
    if os.path.exists(str0):
        shutil.rmtree(str0)


class m3u8:
    def __init__(self, kv):
        if type(kv) == str:
            self.url = kv
            self.temp = "temp0"
            self.size = 64
            self.filename = "result"
        else:
            self.url = kv.get('url')
            self.temp = kv.get('temp') or "temp0"
            self.size = kv.get('size') or 64
            self.filename = kv.get('filename') or "result"

    # 只获取分析结果
    def analysis(self):
        # 获取第一个m3u8
        text = requests.get(self.url).text
        print("解析（1/4）")
        # 获取第二个m3u8
        text = step0(text, self.url)
        print("解析（2/4）")
        # 对内容进行分析
        info = step1(text)
        return info

    # 直接下载
    def download(self):
        # 获取分析结果
        info = self.analysis()
        # 创建缓存文件夹
        rebuildTemp(self.temp)
        print("创建缓存文件夹")
        # 开始下载
        downAll(info.get('list'), info.get('key'), self.temp, self.size)
        # 准备合并
        step2(len(info.get('list')), self.temp)
        print()
        print("合并（1/2）")
        # 进行合并
        step3(self.temp, self.filename)
        print("合并（2/2）")
        # 删除缓存文件夹
        removeTemp(self.temp)
        print("删除缓存文件夹")
        print("OK")


def download(param0):
    m3u8(param0).download()
