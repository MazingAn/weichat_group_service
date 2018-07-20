import itchat
import re
import settings
from itchat.content import *
from dbtools import Record
from pages import render_records

@itchat.msg_register(TEXT, isGroupChat=True)
def text_reply(msg):
		text = msg['Text']
		matched = re.match(r'^#\w+#', text)
		if not matched is None:
			command = matched.group()[1:-1]
			if command == 'add':
				print(msg['ActualNickName'])
				record = Record(nickname=msg['ActualNickName'], content=msg['Text'])
				record.save()
			elif command in 'day week month year':
				records = Record.rows(time_span=command)
				render_records(time_span=command, records=records)
				result_msg = "@{} I'll show you this page. {}".format(msg['ActualNickName'], settings.OUT_URL)
				itchat.send(msg=result_msg, toUserName=msg['FromUserName'])

itchat.auto_login(enableCmdQR=2)
itchat.run()
