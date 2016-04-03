# -*- coding: utf-8 -*-

import re
import scrapy
import time
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
			item_prev = HotItem()
			# collect datas:
			item_prev['userId'] = weibo.xpath('div/a[@class="nk"]/text()').extract()[0]
			item['userUrl'] = weibo.xpath('div/a[@class="nk"]/@href').extract()[0]
			item_prev['userUrl'] = item['userUrl']
			print "*********************item_prev********************"
			print item_prev['userUrl'], item_prev['userId']
			yield item_prev
			yield scrapy.Request(item['userUrl'], callback=self.parse_user_info)
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
			pattern_time_minute = re.compile(u'分钟')
			pattern_time_hour = re.compile(u'小时')
			if re.search(pattern_time_minute, time_and_client_split[0]):
				minutes_before_result = re.search(pattern, time_and_client_split[0])
				if minutes_before_result:
					minutes_before = int(minutes_before_result.group())
					current_time = time.time()
					prev_time = current_time - minutes_before * 60
					sent_time = time.localtime(prev_time)
					item['time'] = str('%s-%s-%s %s:%s:%s' % (sent_time[0], sent_time[1], sent_time[2], sent_time[3], sent_time[4], sent_time[5]))
					print "*************time:***********" 
					print type(date)
					print date
					if len(time_and_client_split) > 1:
						item['client'] = u''
						for i in range(1, len(time_and_client_split)):
							item['client'] = item['client'] + ' ' +time_and_client_split[i]
						item['client'] = item['client'].split(' ', 1)[1]
					else:
						item['client'] = 'UnKnown'
			elif re.search(pattern_time_hour, time_and_client_split[0]):
				hours_before_result = re.search(pattern_time_hour, time_and_client_split[0])
				if hours_before_result:
					hours_before = int(hours_before_result.group())
					current_time = time.time()
					prev_time = current_time - hours_before * 3600
					sent_time = time.localtime(prev_time)
					item['time'] = str('%s-%s-%s %s:%s:%s' % (sent_time[0], sent_time[1], sent_time[2], sent_time[3], sent_time[4], sent_time[5]))
					print "*************time:***********" 
					print type(date)
					print date
					if len(time_and_client_split) > 1:
						item['client'] = u''
						for i in range(1, len(time_and_client_split)):
							item['client'] = item['client'] + ' ' +time_and_client_split[i]
						item['client'] = item['client'].split(' ', 1)[1]
					else:
						item['client'] = 'UnKnown'
			else:
				date_numbers = re.findall(pattern, time_and_client_split[0])
				date = ''
				if time_and_client_split[0] == u'今天':
					date = str('%s-%s-%s ' % (time.localtime()[0], time.localtime()[1], time.localtime()[2]))
				elif len(date_numbers) == 2:
					date = str('%s-%s-%s ' % (time.localtime()[0], date_numbers[0], date_numbers[1]))
				elif len(date_numbers) == 3:
					date = str('%s-%s-%s ' % (date_numbers[0], date_numbers[1], date_numbers[2]))
				item['time'] = date + time_and_client_split[1]
				print "*************time:***********" 
				print type(item['time'])
				print item['time']
				if len(time_and_client_split) > 2:
					item['client'] = u''
					for i in range(2, len(time_and_client_split)):
						item['client'] = item['client'] + ' ' +time_and_client_split[i]
					item['client'] = item['client'].split(' ', 1)[1]
				else:
					item['client'] = 'UnKnown'
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

	def parse_user_info(self, response):
		item = HotItem()
		item['userUrl'] = response.url.decode('utf-8')
		tmp_thisPageCanCrawl = response.xpath('//div[@class="u"]//div/span/text()').extract()
		if tmp_thisPageCanCrawl:
			tmp_userid = tmp_thisPageCanCrawl[0]
			item['userId'] = tmp_userid.split()[0]
			item['isSuper'] = False
			item['isCertificated'] = False
			item['isVip'] = False
			rank_imgs = response.xpath('//div[@class="u"]//div[@class="ut"]//img')
			for rank_img in rank_imgs:
				if rank_img.xpath('@alt').extract()[0] == u'达人':
					item['isSuper'] = True
				elif rank_img.xpath('@alt').extract()[0] == 'V':
					item['isCertificated'] = True
				elif rank_img.xpath('@alt').extract()[0] == 'M':
					item['isVip'] = True
			pattern = re.compile(r'[0-9]+')
			tmp_userWeiboAmount = response.xpath('//div[@class="tip2"]/span').extract()[0]
			tmp_userWeiboAmount_re_result = re.search(pattern, tmp_userWeiboAmount)
			if tmp_userWeiboAmount_re_result:
				item['userWeiboAmount'] = int(tmp_userWeiboAmount_re_result.group())
			else:
				item['userWeiboAmount'] = 0
			other_numbers = response.xpath('//div[@class="tip2"]/a')
			for other_number in other_numbers:
				if len(other_number.xpath('text()').extract()) > 0:
					tmp_ustr = other_number.xpath('text()').extract()[0]
					if tmp_ustr[0] == u'关':
						tmp_result = re.search(pattern, tmp_ustr)
						if tmp_result:
							item['userWatchAmount'] = int(tmp_result.group())
					elif tmp_ustr[0] == u'粉':
						tmp_result = re.search(pattern, tmp_ustr)
						if tmp_result:
							item['userFansAmount'] = int(tmp_result.group())
			yield item