import pymysql

BOT_NAME = 'MySpider'

SPIDER_MODULES = ['MySpider.spiders']

NEWSPIDER_MODULE = 'MySpider.spiders'

ROBOTSTXT_OBEY = False

CONCURRENT_REQUESTS_PER_DOMAIN = 1

# 请求等待时长
DOWNLOAD_DELAY = 0.2

# 随机请求等待
# RANDOMIZE_DOWNLOAD_DELAY = True

DEFAULT_REQUEST_HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    ':authority': 'lzacg.one',
    ':method': 'GET',
    ':scheme': 'https',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'max-age=0',
    'referer': 'https://lzacg.one/',
    'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1'
}

# 管道级别顺序
ITEM_PIPELINES = {
    'MySpider.pipelines.GalgamePipelines': 200
}

# 日志级别
LOG_LEVEL = 'ERROR'

