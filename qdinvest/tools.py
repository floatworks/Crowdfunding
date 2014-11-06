#coding:utf-8
#功能类
from models import *
import string,random
from datetime import datetime
from xml.etree import ElementTree
import requests
import re

#查找某个模型的数据是否存在
def CheckExist(model,kwargs):
	objects = model.objects.filter(**kwargs)
	if objects:
		return True
	return False

#随机产生六个数字
def RandCode():
	return string.join(random.sample(['1','2','3','4','5','6','7','8','9','0'], 6)).replace(' ','')

#生成32位token
def GenToken():
	return string.join(random.sample(['1','2','3','4','5','6','7','8','9','0','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'], 32)).replace(' ','')


#调用短信接口，发送随机验证码
'''
def SendRandomCode(u_tel):
	url = 'http://www.duanxin10086.com/sms.aspx'
	code = RandCode()
	content = '【清大众筹】您的验证码为'+code+'。工作人员不会向您索要，请勿向任何人泄漏。'
	payload = {'userid':'7685','account':'tb2014','password':'123456','mobile':u_tel,
				'content':content,'sendTime':'','action':'send','checkcontent':0,
				'taskName':'','countnumber':1,'mobilenumber':1,'telephonenumber':0}
	r = requests.post(url,data=payload)
	xml = ElementTree.fromstring(r.content)
	returnstatus = xml.find("returnstatus").text
	#验证码获取成功
	if returnstatus == 'Success':
		if CheckExist(RANDOMCODE,{'rc_tel':u_tel}):
			randomCode_obj = RANDOMCODE.objects.get(rc_tel__exact = u_tel)
			randomCode_obj.rc_code = code
			randomCode_obj.rc_time = datetime.now()
			randomCode_obj.save()
		else:
			randomCode_obj = RANDOMCODE(rc_tel = u_tel,rc_code = code,rc_time = datetime.now())
			randomCode_obj.save()
		return True
	else:
		return False
'''
#调用短信接口，发送随机验证码
def SendRandomCode(u_tel):
	url = 'http://www.mxtong.net.cn/GateWay/Services.asmx/DirectSend'
	code = RandCode()
	content = '【清大众筹】您的验证码为'+code+'。工作人员不会向您索要，请勿向任何人泄漏。'
	payload = {'UserID':'965125','Account':'admin','Password':'DUWBT2','Phones':u_tel,
				'Content':content,'SendTime':'','SendType':'1','PostFixNumber':''}
	r = requests.get(url,params=payload)
	#xml = ElementTree.fromstring(r.content)
	#RetCode = xml.find("ROOT").find("RetCode").text
	#print RetCode
	search = re.search('<RetCode>(?P<status>\w+)</RetCode>',r.content)
	RetCode = search.groupdict()['status']
	if RetCode == 'Sucess':
		if CheckExist(RANDOMCODE,{'rc_tel':u_tel}):
			randomCode_obj = RANDOMCODE.objects.get(rc_tel__exact = u_tel)
			randomCode_obj.rc_code = code
			randomCode_obj.rc_time = datetime.now()
			randomCode_obj.save()
		else:
			randomCode_obj = RANDOMCODE(rc_tel = u_tel,rc_code = code,rc_time = datetime.now())
			randomCode_obj.save()
		return True
	else:
		return False


#token检查合法性 超时时间为30min
#add = 1 表示插入或者更新token add = 0 检验是否合法
def CheckToken(user,token,add):
	TOKEN_objs = TOKEN.objects.filter(t_user__exact = user)
	if add == 0 and TOKEN_objs:
		if TOKEN_objs[0].t_token == token:
			if (datetime.now() - TOKEN_objs[0].t_time).seconds < 1800:
				TOKEN_objs[0].t_time = datetime.now()
				TOKEN_objs[0].save()
				return True
			else:
				return False
		else:
			return False
	elif add == 1:
		if TOKEN_objs:
			TOKEN_objs[0].t_time = datetime.now()
			TOKEN_objs[0].t_token = token
			TOKEN_objs[0].save()
		else:
			TOKEN_new = TOKEN(t_user = user,t_token = token,t_time = datetime.now())
			TOKEN_new.save()
		return False