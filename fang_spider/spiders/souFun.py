# -*- coding: utf-8 -*-
import scrapy
import re
from fang_spider.items import NewHouseItem
from fang_spider.items import ESFHouseItem

from scrapy_redis.spiders import RedisSpider

class SoufunSpider(RedisSpider): #(scrapy.Spider)
    name = 'souFun'
    allowed_domains = ['fang.com']
    # start_urls = ['https://www.fang.com/SoufunFamily.htm']
    redis_key = "fang:start_urls" #现在是从redis中读取开始url

    def parse(self, response):
        trs = response.xpath('//div[@class="outCont"]//tr')
        province = None
        for tr in trs:
            tds = tr.xpath('.//td[not(@class)]')
            province_td = tds[0]
            province_text = province_td.xpath('.//text()').get()
            province_text = re.sub(r"\s", "", province_text)
            if province_text:
                province = province_text

            if province == '其它':
                continue

            city_td = tds[1]
            city_links = city_td.xpath(".//a")
            for city_link in city_links:
                city = city_link.xpath('.//text()').get()
                city_url = city_link.xpath('.//@href').get()
                # 构建新房的url链接
                url_module = city_url.split('//')
                # scheme = url_module[0] http
                domain = url_module[1]
                domain_lit = domain.split('.')
                domain_city = domain_lit[0]
                domain_fang = domain_lit[1] + '.' + domain_lit[2]

                if 'bj.' in domain:
                    newhouse_url = "https://newhouse.fang.com/house/s/"
                    esf_url = "：https://esf.fang.com/"
                else:
                    newhouse_url = 'https://' + domain_city + '.newhouse.' + domain_fang + 'house/s/'
                    # 构建二手房链接
                    esf_url = 'https://' + domain_city + '.esf.' + domain_fang

                yield scrapy.Request(url=newhouse_url, callback=self.parse_newhouse, meta={'info': (province, city)})

                yield scrapy.Request(url=esf_url, callback=self.parse_esf, meta={'info': (province, city)})



    def parse_newhouse(self, response):
        province, city = response.meta.get('info')
        lis = response.xpath("//div[contains(@class,'nl_con')]/ul/li")
        for li in lis:
            name = li.xpath('.//div[@class="nlcd_name"]/a/text()').get()
            if name:
                name = name.strip()
            house_type_list = li.xpath(".//div[contains(@class,'house_type')]/a/text()").getall()
            house_type_list = list(map(lambda x: re.sub(r'\s', '', x), house_type_list))
            rooms = list(filter(lambda x: x.endswith('居'), house_type_list))
            area = "".join(li.xpath(".//div[contains(@class,'house_type')]/text()").getall())
            area = re.sub(r"\s|－|/", '', area)
            address = li.xpath(".//div[@class='address']/a/@title").get()
            district_text = "".join(li.xpath(".//div[@class='address']/a//text()").getall())
            district_text = re.sub(r'\s|', '', district_text)

            # print(district_text)
            district_text = re.search(r'.*\[(.+)\].*', district_text)
            if district_text:
                district = district_text.group(1)
            sale = li.xpath('.//div[contains(@class,"fangyuan")]/span/text()').get()
            price = "".join(li.xpath('.//div[@class="nhouse_price"]/span/text()').getall())
            origin_url = li.xpath('.//div[@class="nlcd_name"]/a/@href').get()
            origin_url = response.urljoin(origin_url)

            item = NewHouseItem(name=name, rooms=rooms, area=area, address=address, district=district, sale=sale,
                                price=price, origin_url=origin_url, province=province, city=city)
            yield item

        next_url = response.xpath('//div[@class="page"]//a[@class="next"]/@href').get()
        if next_url:
            yield scrapy.Request(url=response.urljoin(next_url), callback=self.parse_newhouse,meta={'info':(province,city)})

    def parse_esf(self, response):
        province, city = response.meta.get('info')

        dls = response.xpath('//div[contains(@class,"shop_list")]/dl')
        for dl in dls:
            item = ESFHouseItem(province=province, city=city)
            item['name'] = dl.xpath('.//p[@class="add_shop"]/a/@title').get()
            infos = dl.xpath('.//p[@class="tel_shop"]/text()').getall()
            infos = list(map(lambda x: re.sub(r'\s', '', x), infos))
            for info in infos:
                if "厅" in info:
                    item['rooms'] = info
                elif "层" in info:
                    item['floor'] = info
                elif "向" in info:
                    item['toward'] = info
                elif "㎡" in info:
                    item['area'] = info
                elif "建" in info:
                    item['year'] = info
            item['address'] = dl.xpath('.//p[@class="add_shop"]/span/text()').get()
            item['price'] = ''.join(dl.xpath('.//dd[@class="price_right"]/span[1]//text()').getall())
            item['unit'] = dl.xpath('.//dd[@class="price_right"]/span[2]/text()').get()
            detall_url = dl.xpath('.//h4[@class="clearfix"]/a/@href').get()
            item['oringin_url'] = response.urljoin(detall_url)
            yield item

        next_url = response.xpath('//div[@id="list_D10_15"]//p[1]/a/@href').get()

        if next_url:
            yield scrapy.Request(url=response.urljoin(next_url), callback=self.parse_esf,meta={'info': (province, city)})
