import os
from urllib.parse import unquote, urlparse

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from loguru import logger
from tqdm import tqdm

headers = {'User-Agent': UserAgent().random}


def get_img_src(url: str, set_proxy=False):
    if set_proxy:
        os.environ["https_proxy"] = "http://127.0.0.1:7890"
    res = requests.get(url, headers=headers, timeout=5)
    logger.info(f'{res.status_code} {unquote(res.request.url)}')
    page = BeautifulSoup(res.text, 'html.parser')
    # 获取 img 标签
    imgs = page.find_all('img')
    # 获取标签中的 src
    img_urls = [img.get('src') for img in imgs]
    return img_urls


def get_file_name(url):
    return os.path.basename(urlparse(url).path)


def get_file_size(url):
    size = int(requests.head(url).headers['Content-Length'])
    return size


def download(urls, folder, set_proxy):
    # 创建下载目录
    if not os.path.exists(folder):
        os.mkdir(folder)
    # 保证下载目录以斜杆结尾
    if not (folder.endswith('/') or folder.endswith('\\')):
        folder += '/'
    if set_proxy:
        os.environ["https_proxy"] = "http://127.0.0.1:7890"
    s = requests.session()
    for url in tqdm(urls, colour='green'):
        file_name = get_file_name(url)
        with open(folder + file_name, 'wb') as f:
            r = s.get(url, headers=headers, timeout=5)
            f.write(r.content)


def github_releases_latest_version(owner: str, repo: str) -> str:
    """
    获取 release 最新版本
    """
    api = f'https://api.github.com/repos/{owner}/{repo}/releases/latest'
    latest_dict = requests.get(api, headers=headers).json()
    version = latest_dict['tag_name']
    return version


def ip2deciaml(ip):
    decimal = 0
    parts = ip.split('.')[::-1]
    parts = [eval(i) for i in parts]
    for i, part in enumerate(parts):
        result = part * 256 ** i
        decimal += result
    return decimal


def ip2octal(ip):
    decimal = ip2deciaml(ip)
    # 去掉八进制的标记 o
    octal = '0' + oct(decimal)[2:]
    return octal


def ip2hexadecimal(ip):
    decimal = ip2deciaml(ip)
    hexadecimal = hex(decimal)
    return hexadecimal


if __name__ == '__main__':
    pass
