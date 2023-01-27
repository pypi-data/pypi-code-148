import os
import time

from sparrow import rel_to_abs, rm
import requests
from tqdm import tqdm
import sys


class Installer:
    proxy_prefix = "https://ghproxy.com/"
    frp_dir = rel_to_abs('./frp/', return_str=True)

    def __init__(self, frp_version="0.44.0", platform='linux', framework='amd64', china_source=True, use_httpie=True):
        """
        platform: "linux", "darwin", "windows", "freebsd"
        framework: "amd64","arm", "arm64", "386", "mips64"
        """
        file_suffix = "zip" if platform == "windows" else "tar.gz"
        frp_release_name = f"frp_{frp_version}_{platform}_{framework}.{file_suffix}"
        frp_unpack_name = f"frp_{frp_version}_{platform}_{framework}"
        self.frp_release_name = frp_release_name
        self.frp_release_file_path = os.path.join(self.frp_dir, self.frp_release_name)
        self.frp_unpack_file_dir = os.path.join(self.frp_dir, frp_unpack_name)
        self.frp_download_url = f"https://github.com/fatedier/frp/releases/download/v{frp_version}/{frp_release_name}"
        self._china_source = china_source
        self._use_httpie = use_httpie

    def clean_dir(self):
        rm(self.frp_dir)
        rm(self.frp_release_file_path)

    def install(self):
        self.download_frp()
        time.sleep(0.1)
        self.unpack()

    def unpack(self):
        os.system(f"sparrow unpack {self.frp_release_file_path} {self.frp_dir}")

    def download_frp(self):
        if not os.path.exists(self.frp_dir):
            os.mkdir(self.frp_dir)
        url = f"{self.proxy_prefix}{self.frp_download_url}" if self._china_source else self.frp_download_url
        # print(self.frp_release_file_path)
        if self._use_httpie:
            os.system(f"http -d {url} -o {self.frp_release_file_path}")
        else:
            response = requests.get(url, stream=True)
            total = response.headers.get('content-length')
            with open(self.frp_release_file_path, 'wb') as f:
                if total is None:
                    for chunk in tqdm(response.iter_content(chunk_size=1024*500)):
                        f.write(chunk)
                else:
                    downloaded = 0
                    total = int(total)
                    print(f"Downloading {self.frp_release_name} of size {total/1024/1024:.2f} Mb...")
                    for chunk in response.iter_content(chunk_size=max(int(total/1000), 1024*1024)):
                        downloaded += len(chunk)
                        f.write(chunk)
                        done = int(50 * downloaded / total)
                        sys.stdout.write('\r[{}{}]'.format('█' * done, '.' * (50 - done)))
                        sys.stdout.flush()
                    print('\nDone.')


if __name__ == "__main__":
    ins = Installer()
    ins.clean_dir()
    ins.install()
    # ins.unpack()
