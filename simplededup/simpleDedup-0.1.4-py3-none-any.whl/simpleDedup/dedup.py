import json
import hashlib
from functools import wraps
from urllib.parse import urlparse, urlencode, parse_qs
import os
import redis



class URLFilter:
    def __init__(self, file_path: str = "url_records.json", enable_fingerprint: bool = False):
        self.crawled_urls = set()
        self.failed_urls = set()
        self.file_path = file_path
        self.enable_fingerprint = enable_fingerprint
        
    def _normalize_url(self, url: str) -> str:
        parsed_url = urlparse(url)
        query = parse_qs(parsed_url.query)
        query = {k: v[0] for k, v in query.items()}
        query = sorted(query.items(), key=lambda x: x[0])
        query = urlencode(query)
        url = parsed_url._replace(query=query).geturl()
        return url
    
    def _generate_fingerprint(self, url: str) -> str:
        fp = hashlib.sha1(url.encode()).hexdigest()
        return fp
        # pass  # 用任意hash算法生成指纹
    
    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if "url" in kwargs:
                url = kwargs.get("url")
            else:
                url = args[0]
            normalized_url = self._normalize_url(url)
            if self.enable_fingerprint:
                fingerprint = self._generate_fingerprint(normalized_url)
                if fingerprint in self.crawled_urls:
                    return None
                self.crawled_urls.add(fingerprint)
            else:
                if normalized_url in self.crawled_urls:
                    return None
                self.crawled_urls.add(normalized_url)
            try:
                response = func(*args, **kwargs)
                return response
            except Exception as e:
                self.failed_urls.add(normalized_url)
                raise e
            finally:
                filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.file_path)
                with open(filename, "w") as f:
                    # data = json.dumps({"crawled": list(self.crawled_urls), "failed": list(self.failed_urls)})
                    # f.write(data)
                    json.dump({"crawled": list(self.crawled_urls), "failed": list(self.failed_urls)}, f)
                print("write to file successfully")
        return wrapper




class RedisURLFilter(URLFilter):
    def __init__(self, redis_host: str = "localhost", redis_port: int = 6379, 
                 redis_db: int = 0, redis_password: str = None, 
                 enable_fingerprint: bool = False):
        super().__init__(enable_fingerprint)
        self.redis_client = redis.Redis(host=redis_host, port=redis_port, db=redis_db, password=redis_password)
        self.crawled_key = "crawled_urls"
        self.failed_key = "failed_urls"
        
    def _check_redis(self, key, url):
        if self.enable_fingerprint:
            fingerprint = self._generate_fingerprint(url)
            if self.redis_client.sismember(key, fingerprint):
                return True
            self.redis_client.sadd(key, fingerprint)
        else:
            if self.redis_client.sismember(key, url):
                return True
            self.redis_client.sadd(key, url)
        return False
        
    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if "url" in kwargs:
                url = kwargs.get("url")
            else:
                url = args[0]
            normalized_url = self._normalize_url(url)
            if self._check_redis(self.crawled_key, normalized_url):
                return None
            try:
                response = func(*args, **kwargs)
                return response
            except Exception as e:
                self._check_redis(self.failed_key, normalized_url)
                raise e
            finally:
                filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.file_path)
                with open(filename, "w") as f:
                    json.dump({"crawled": list(self.redis_client.smembers(self.crawled_key)), 
                               "failed": list(self.redis_client.smembers(self.failed_key))}, f)
                print("write to file successfully")
        return wrapper




import requests

@URLFilter(enable_fingerprint=True)
def test_crawl(url = "http://www.baidu.com"): 
    r = requests.get(url)
    return r


if __name__ == "__main__":
    url = "http://www.baidu.com"
    test_crawl(url)