# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import signals
import json
import codecs
import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi

class MySQLStoreHotPipeline(object):
	def __init__(self, dbpool):
		self.dbpool = dbpool

	@classmethod
	def from_settings(cls, settings):
		dbargs = dict(
			host = settings['MYSQL_HOST'],
			db = settings['MYSQL_DBNAME'],
			user = settings['MYSQL_USER'],
			passwd = settings['MYSQL_PASSWD'],
			charset = 'utf8',
			# cursorclass = MySQLdb.cursors.DictCursor,
			use_unicode = True,
		)
		dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
		return cls(dbpool)

	def process_item(self, item, spider):
		print "pipeline.py->process_item"
		deferred = self.dbpool.runInteraction(self._do_upsert, item, spider)
		return deferred

	def _do_upsert(self, conn, item, spider):			
		print "***********************************************************************"
		print type(item["support"])
		select_sql = 'SELECT * FROM Hot_1 WHERE userid = %s AND time = %s'
		update_sql = 'UPDATE Hot_1 SET issuper = %d, iscertificated = %d, isvip = %d, issthelse = %d, weibotext = %s, support = %d, relay = %d, comment = %d, client = %s WHERE userid = %s AND time = %s'
		insert_sql = 'INSERT INTO Hot_1(userid, issuper, iscertificated, isvip, issthelse, weibotext, support, relay, comment, time, client) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
		conn.execute(select_sql, (item["userId"], item["time"]))
		select_res = conn.fetchone()
		if select_res:

			conn.execute(update_sql, (item["isSuper"], item["isCertificated"], item["isVip"], item["isSthelse"], item["weibotext"], item['support'], item['relay'], item['comment'], item['client'], item['userId'], item['time']))
		else:
			conn.execute(insert_sql, (item["userId"], item["isSuper"], item["isCertificated"], item["isVip"], item["isSthelse"], item["weibotext"], item['support'], item['relay'], item['comment'], item['time'], item['client']))
		return item
# 
# 