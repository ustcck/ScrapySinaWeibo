# -*- coding: utf-8 -*-

import pynlpir
import MySQLdb
# import sys

# reload(sys)
# sys.setdefaultencoding('utf-8')

conn= MySQLdb.connect(
	host='localhost',
	port = 3306,
	user='root',
	passwd='1111',
	db ='sinadb',
	charset='utf8'
)
cur = conn.cursor()
pynlpir.open()

res = cur.execute("SELECT weibotext FROM hot_1_user_weibo WHERE UNIX_TIMESTAMP(time) > UNIX_TIMESTAMP('2016-4-3 12:00:00')")
info = cur.fetchmany(res)
nlpir_results = pynlpir.segment(info[0][0])
for nlpir_result in nlpir_results:
	print nlpir_result[0], nlpir_result[1]


# pynlpir.open()
# s = u':【东北衰败宣告了国企城市的破产 】东北衰落的原因很简单，那就是经济被国企吸干了。东北是全球苏联式经济的最佳典范。苏联计划经济已经垮台了，东北国企还在苟延残喘……'
# print s
# for x in pynlpir.segment(s):
# 	print x[0], x[1]