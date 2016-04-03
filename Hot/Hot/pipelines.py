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
		if 'userFansAmount' in item:
			deferred = self.dbpool.runInteraction(self._do_upsert_user, item, spider)
		elif 'weibotext' in item:
			deferred = self.dbpool.runInteraction(self._do_upsert_weibo, item, spider)
		elif 'userUrl' in item:
			deferred = self.dbpool.runInteraction(self._do_upsert_user_urlandid, item, spider)
		else:
			"I CHOOSE GO DIE!!!"
		return deferred

	def _do_upsert_user_urlandid(self, conn, item, spider):
		print "**********************_do_upsert_user_urlanlid_***************************"
		select_sql = 'SELECT * FROM Hot_1_user WHERE userurl = %s'
		insert_sql = 'INSERT INTO Hot_1_user(userurl, userid) VALUES (%s, %s)'
		update_sql = 'UPDATE Hot_1_user SET userid = %s WHERE userurl = %s'
		conn.execute(select_sql, (item["userUrl"], ))
		select_res = conn.fetchone()
		if select_res:
			conn.execute(update_sql, (item["userId"], item["userUrl"]))
		else:
			conn.execute(insert_sql, (item["userUrl"], item["userId"]))
		return item

	def _do_upsert_user(self, conn, item, spider):
		print "**************************_do_upsert_user_********************************"
		select_sql = 'SELECT * FROM Hot_1_user WHERE userurl = %s'
		update_sql = 'UPDATE Hot_1_user SET userid = %s, userfansamount = %s, userwatchamount = %s, userweiboamount = %s, issuper = %s, iscertificated = %s, isvip = %s WHERE userurl = %s'
		insert_sql = 'INSERT INTO Hot_1_user(userurl, userid, userfansamount, userwatchamount, userweiboamount, issuper, iscertificated, isvip, issthelse) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
		conn.execute(select_sql, (item["userUrl"], ))
		select_res = conn.fetchone()
		if select_res:
			conn.execute(update_sql, (item["userId"], item["userFansAmount"], item["userWatchAmount"], item["userWeiboAmount"], item["isSuper"], item["isCertificated"], item["isVip"], item["userUrl"]))
		else:
			conn.execute(insert_sql, (item["userUrl"], item["userId"], item["userFansAmount"], item["userWatchAmount"], item["userWeiboAmount"], item["isSuper"], item["isCertificated"], item["isVip"]))
		return item

	def _do_upsert_weibo(self, conn, item, spider):			
		print "*************************_do_upsert_weibo_********************************"
		select_sql = 'SELECT * FROM Hot_1_user_weibo WHERE userurl = %s AND time = %s'
		update_sql = 'UPDATE Hot_1_user_weibo SET weibotext = %s, support = %s, relay = %s, comment = %s, client = %s WHERE userurl = %s AND time = %s'
		insert_sql = 'INSERT INTO Hot_1_user_weibo(userurl, weibotext, support, relay, comment, time, client) VALUES (%s, %s, %s, %s, %s, %s, %s)'
		conn.execute(select_sql, (item["userUrl"], item["time"]))
		select_res = conn.fetchone()
		if select_res:
			conn.execute(update_sql, (item["weibotext"], item['support'], item['relay'], item['comment'], item['client'], item['userUrl'], item['time']))
		else:
			conn.execute(insert_sql, (item["userUrl"], item["weibotext"], item['support'], item['relay'], item['comment'], item['time'], item['client']))
		return item
# 
# 