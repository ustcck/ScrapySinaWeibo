# -*- coding: utf-8 -*-

import pynlpir
# import MySQLdb

# conn= MySQLdb.connect(
# 	host='localhost',
# 	port = 3306,
# 	user='root',
# 	passwd='1111',
# 	db ='sinadb',
# )
# cur = conn.cursor()

pynlpir.open()
s = u':【东北衰败宣告了国企城市的破产 】东北衰落的原因很简单，那就是经济被国企吸干了。东北是全球苏联式经济的最佳典范。苏联计划经济已经垮台了，东北国企还在苟延残喘……'
print s
for x in pynlpir.segment(s):
	print x[0], x[1]