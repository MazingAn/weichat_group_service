# -*- coding:utf-8 -*-
import MySQLdb
import logger
import settings
import sys
reload(sys)  
sys.setdefaultencoding('utf8')   

class Record:
	'''Record Model'''
	def __init__(self, nickname, content):
		self.nickname = nickname
		self.content = content
		self.conn = None
		self.cursor = None
	
	def _check_params(self):
		return len(self.nickname) > 0 and len(self.content) > 0

	def _init_db(self):
		'''init database whith create a table named record'''
		try:
			if self.conn is None:
				self.conn = MySQLdb.connect(settings.DB_HOST, settings.DB_USER, settings.DB_PASSWORD, settings.DB_NAME, charset='utf8')
				self.cursor = self.conn.cursor()
			self.cursor.execute("CREATE TABLE IF NOT EXISTS record \
								(nickname VARCHAR(64),\
								content VARCHAR(1024),\
								pub_time DATETIME)")
			self.conn.commit()	
		except Exception as e:
			logger.e('failed to create table on {}; {}'.format(settings.DB_NAME, str(e)))	
	
	def _close_db(self):
		'''close databse'''	
		if not self.cursor is None:
			self.cursor = None
		if not self.conn is None:
			self.conn = None
	
	def save(self):
		'''save a record to database'''
		try:
			self._init_db()	
			sql = 'INSERT INTO record VALUES("{}", "{}", NOW())'.format(self.nickname, self.content)
			print(sql)
			self.cursor.execute(sql)
			self.conn.commit()
			self._close_db()
		except Exception as e:
			logger.e('failed to insert row; {}'.format(str(e)))

	@staticmethod
	def rows(time_span='week'):
		'''select rows from record during a time span,
		the time span can be: day, week, month, year
		'''
		conn = MySQLdb.connect(settings.DB_HOST, settings.DB_USER, settings.DB_PASSWORD, settings.DB_NAME, charset='utf8')
		cursor = conn.cursor()
		if time_span == 'day':
			sql = "SELECT * FROM record WHERE TO_DAYS(pub_time) = TO_DAYS(NOW())"
		elif time_span == 'week':
			sql = "SELECT * FROM record WHERE YEARWEEK(date_format(pub_time,'%Y-%m-%d')) = YEARWEEK(NOW())"
		elif time_span == 'month':
			sql = "SELECT * FROM record WHERE DATE_FORMAT(pub_time, '%Y%m' ) = DATE_FORMAT( CURDATE( ) , '%Y%m')"
		else:
			sql = "SELECT * FROM record WHERE YEAR(pub_time)=YEAR(NOW())"
		try:
			cursor.execute(sql)
			results = cursor.fetchall()
			cursor.close()
			conn.close()
			return results
		except Exception as e:
			logger.e('failed to query data from database; {}'.format(str(e)))
