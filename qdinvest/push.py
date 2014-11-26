#coding:utf-8
import jpush as jpush
import traceback
#调用极光推送，推送消息
JPUSH_APP_KEY = u'ba136f5689812e6dc34eb516'
JPUSH_MasterSecret = u'77619609fe412e68f923bc0f'
_jpush = jpush.JPush(JPUSH_APP_KEY,JPUSH_MasterSecret)

def PushMessage(alert,title,n_type,n_id):
	push = _jpush.create_push()
	push.audience = jpush.all_
	push.notification = jpush.notification(
		ios=jpush.ios(
			alert=alert,
			extras={"n_type":n_type,"n_id":n_id}
			),
		android=jpush.android(
			alert=alert,
			title=title,
			extras={"n_type":n_type,"n_id":n_id}
			)
		)
	push.platform = jpush.platform('ios', 'android')
	try:
		push.send()
	except:
		traceback.print_exc()
