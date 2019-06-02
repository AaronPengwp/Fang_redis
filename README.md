搜房网分布式爬虫
1、获取所有城市的url链接
     https://www.fang.com/SoufunFamily.htm
2、获取所有城市的新房的url链接
     例：深圳：https://sz.fang.com/
     深圳新房：https://sz.newhouse.fang.com/house/s/
3、获取所有城市的新房的url链接
     例：深圳：https://sz.fang.com/
     深圳二手房：https://sz.esf.fang.com/
北京是个例外：
    北京的新房链接：https://newhouse.fang.com/house/s/
    北京的二手房链接：https://esf.fang.com/

要将一个Scrapy项目变成一个Scrapy-redis项目只需修改以下三点就可以了：

  1、将爬虫的类从scrapy.Spider变成scrapy_redis.spiders.RedisSpider；或者是从scrapy.CrawlSpider变成scrapy_redis.spiders.RedisCrawlSpider。

  2、将爬虫中的start_urls删掉。增加一个redis_key="xxx"。这个redis_key是为了以后在redis中控制爬虫启动的。爬虫的第一个url，就是在redis中通过这个发送出去的。
  3、在配置文件中增加如下配置：
# Scrapy-Redis相关配置
# 确保request存储到redis中
SCHEDULER = "scrapy_redis.scheduler.Scheduler"

# 确保所有爬虫共享相同的去重指纹
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

# 设置redis为item pipeline
ITEM_PIPELINES = {
    'scrapy_redis.pipelines.RedisPipeline': 300
}

# 在redis中保持scrapy-redis用到的队列，不会清理redis中的队列，从而可以实现暂停和恢复的功能。
SCHEDULER_PERSIST = True

# 设置连接redis信息
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379

运行爬虫：
   在爬虫服务器上。进入爬虫文件所在的路径，然后输入命令：scrapy runspider [爬虫名字]。
   在Redis服务器上，推入一个开始的url链接：redis-cli> lpush [redis_key] start_url开始爬取。

