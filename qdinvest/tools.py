#coding:utf-8
#功能类
from models import *
import string,random
from datetime import datetime

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