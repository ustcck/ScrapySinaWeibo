# -*- coding: utf-8 -*-

import re
import scrapy
from Hot.items import HotItem

class HotSpider(scrapy.Spider):
	name = 'Hot'
	start_urls = [
		'http://weibo.cn/pub/topmblog'
	]

	def parse(self, response):
		url_prefix = 'http://weibo.cn'
		weibos = response.xpath('//div[@id!="pagelist"]')
		for weibo in weibos:
			item = HotItem()
			# initial item:
			item['isSuper'] = False
			item['isCertificated'] = False
			item['isVip'] = False
			item['isSthelse'] = False
			# collect datas:
			rank_imgs = weibo.xpath('div/img')
			for rank_img in rank_imgs:
				if rank_img.xpath('@alt').extract()[0] == u'达人':
					item['isSuper'] = True
				elif rank_img.xpath('@alt').extract()[0] == 'V':
					item['isCertificated'] = True
				elif rank_img.xpath('@alt').extract()[0] == 'M':
					item['isVip'] = True
				else:
					item['isSthelse'] = True
			# print item['isSuper'], item['isCertificated'], item['isVip'], item['isSthelse']
			item['userId'] = weibo.xpath('div/a[@class="nk"]/text()').extract()[0]
			# print item['userId']
			texts = weibo.xpath('div/span[@class="ctt"]/text()')
			item['weibotext'] = u''
			for text in texts.extract():
				for tmp_uchar in text:
					try:
						item['weibotext'] = item['weibotext'] + tmp_uchar.encode('gbk')
					except UnicodeEncodeError:
						item['weibotext'] = item['weibotext']
					except UnicodeDecodeError:
						item['weibotext'] = item['weibotext'] + tmp_uchar
			# print item['weibotext']
			numbers = weibo.xpath('div/a')
			pattern = re.compile(r'[0-9]+')
			for number in numbers:
				if len(number.xpath('text()').extract()) > 0:
					tmp_ustr = number.xpath('text()').extract()[0]
					if tmp_ustr[0] == u'赞':
						tmp_result = re.search(pattern, tmp_ustr)
						if tmp_result:
							item['support'] = int(tmp_result.group())
					elif tmp_ustr[0] == u'转':
						tmp_result = re.search(pattern, tmp_ustr)
						if tmp_result:
							item['relay'] = int(tmp_result.group())
					elif tmp_ustr[0] == u'评':
						tmp_result = re.search(pattern, tmp_ustr)
						if tmp_result:
							item['comment'] = int(tmp_result.group())
			# print item['support'], item['relay'], item['comment']
			time_and_client = weibo.xpath('div/span[@class="ct"]/text()').extract()[0]
			time_and_client_split = time_and_client.split()
			item['time'] = time_and_client_split[0] + ' ' + time_and_client_split[1]
			if len(time_and_client_split) > 2:
				item['client'] = u''
				for i in range(2, len(time_and_client_split)):
					item['client'] = item['client'] + ' ' +time_and_client_split[i]
				item['client'] = item['client'].split(' ', 1)[1]
			else:
				item['client'] = 'UnKnown'
			# print item['time'], "********************", item['client']
			yield item
		# find next page
		url_suffix = ''
		pages = response.xpath('//div[@id="pagelist"]/form/div/a')
		for page in pages:
			if page.xpath('text()').extract()[0] == u'下页':
				url_suffix = page.xpath('@href').extract()[0]
				url_next = url_prefix + url_suffix
				yield scrapy.Request(url_next, self.parse)
				break
