# Scrapy settings for goldendoodle project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'Goldendoodle'

SPIDER_MODULES = ['goldendoodle.spiders']
NEWSPIDER_MODULE = 'goldendoodle.spiders'

# Logging
LOG_FORMAT = '%(asctime)s-[%(levelname)s]-%(name)s:%(lineno)d:%(message)s'
# Minimum level to log. Available levels are: CRITICAL, ERROR, WARNING, INFO, DEBUG. For more info see Logging.
# TODO change to ERROR when syncing to Master
#LOG_LEVEL = 'DEBUG'
LOG_LEVEL = 'ERROR'
LOG_ENABLED = True

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'goldendoodle (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False  # True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# see https://docs.scrapy.org/en/latest/topics/settings.html
#DOWNLOAD_HANDLERS = {
#    'https': 'scrapy.core.downloader.handlers.http2.#H2DownloadHandler',
#}

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'goldendoodle.middlewares.GoldendoodleSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'goldendoodle.middlewares.GoldendoodleDownloaderMiddleware': 543,
#}

DOWNLOADER_MIDDLEWARES = {"scrapy_selenium_middleware.SeleniumDownloader": 451}
CONCURRENT_REQUESTS = 1  # multiple concurrent browsers are not supported yet
SELENIUM_IS_HEADLESS = False
# SELENIUM_PROXY = (
#     "http://user:password@my-proxy-server:port"  # set to None to not use a proxy
# )
SELENIUM_PROXY = None
SELENIUM_USER_AGENT = "User-Agent: Mozilla/5.0"
# a list of regular expression to record the incoming requests by matching the url
# recorded requests can be found on driver.requests property
SELENIUM_REQUEST_RECORD_SCOPE = [".*"] # This will record all requests
SELENIUM_FIREFOX_PROFILE_SETTINGS = {}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'goldendoodle.pipelines.GoldendoodlePipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
