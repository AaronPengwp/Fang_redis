# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewHouseItem(scrapy.Item):
      # 省份
      province = scrapy.Field()
      # 城市
      city = scrapy.Field()
      # 城市小区名字
      name = scrapy.Field()
      # 价格
      price = scrapy.Field()
      # 几居，这个是个列表
      rooms = scrapy.Field()
      # 面积
      area = scrapy.Field()
      # 地址
      address = scrapy.Field()
      # 行政区
      district = scrapy.Field()
      # 是否在售
      sale = scrapy.Field()
      # 房天下的详情页面url
      origin_url = scrapy.Field()


class ESFHouseItem(scrapy.Item):
      # 省份
      province = scrapy.Field()
      # 城市
      city = scrapy.Field()
      # 地小区名字
      name = scrapy.Field()
      # 几室几厅
      rooms = scrapy.Field()
      # 层
      floor = scrapy.Field()
      # 朝向
      toward = scrapy.Field()
      # 年代
      year = scrapy.Field()
      # 地址
      address = scrapy.Field()
      # 建筑面积
      area = scrapy.Field()
      # 总价
      price = scrapy.Field()
      # 单价
      unit = scrapy.Field()
      # 原始的URL
      oringin_url = scrapy.Field()