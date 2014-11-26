#coding:utf-8
import jpush as jpush
import traceback
#调用极光推送，推送消息
JPUSH_APP_KEY = u'ba136f5689812e6dc34eb516'
JPUSH_MasterSecret = u'77619609fe412e68f923bc0f'
_jpush = jpush.JPush(JPUSH_APP_KEY,JPUSH_MasterSecret)

def PushMessage(msg):
	
	push = _jpush.create_push()
	push.audience = jpush.all_
	print msg
	push.notification = jpush.notification(alert=msg)
	push.platform = jpush.all_

	try:
		push.send()
	except:
		traceback.print_exc()
