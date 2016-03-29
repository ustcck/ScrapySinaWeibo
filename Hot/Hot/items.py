# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HotItem(scrapy.Item):
	# define the fields for your item here like:
	# name = scrapy.Field()
	userId = scrapy.Field()			#用户昵称
	isSuper = scrapy.Field()		#用户是否是达人
	isCertificated = scrapy.Field()	#用户是否认证(大V)
	isVip = scrapy.Field()			#用户是否是会员
	isSthelse = scrapy.Field()		#检验是否还有别的身份
	weibotext = scrapy.Field()		#微博正文
	support = scrapy.Field()		#微博点赞数
	relay = scrapy.Field()			#微博转发数
	comment = scrapy.Field()		#微博评论数
	time = scrapy.Field()			#微博发布时间
	client = scrapy.Field()			#用户客户端




