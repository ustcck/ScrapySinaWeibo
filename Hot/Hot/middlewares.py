import random
import base64
# from settings import PROXIES
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware

class RandomUserAgent(object):

	def __init__(self, agents):
		self.agents = agents

	@classmethod
	def from_crawler(cls, crawler):
		return cls(crawler.settings.getlist('USER_AGENTS'))

	def process_request(self, request, spider):
		x = random.choice(self.agents)
		print "**************************" + x
		request.headers.setdefault('User-Agent', x)

# class ProxyMiddleware(object):
# 	def process_request(self, request, spider):
# 		proxy = random.choice(PROXIES)
# 		if proxy['user_pass'] is not None:
# 			request.meta['proxy'] = "http://%s" % proxy['ip_port']
# 			encoded_user_pass = base64.encodestring(proxy['user_pass'])
# 			request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass
# 			print "**************ProxyMiddleware have pass************" + proxy['ip_port']
# 		else:
# 			print "**************ProxyMiddleware no pass************" + proxy['ip_port']
# 			request.meta['proxy'] = "http://%s" % proxy['ip_port']