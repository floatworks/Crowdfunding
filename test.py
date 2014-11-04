#coding:utf-8
import os
os.environ['DJANGO_SETTINGS_MODULE'] = "Crowdfunding.settings"
import requests
import qdinvest.tools as T

url = 'http://www.duanxin10086.com/sms.aspx'
code = T.RandCode()
content = '【清大众筹】您的验证码为'+code+'。工作人员不会向您索要，请勿向任何人泄漏。'
payload = {'userid':'7685','account':'tb2014','password':'123456','mobile':'13136652521',
						'content':content,'sendTime':'','action':'send','checkcontent':0,
						'taskName':'','countnumber':1,'mobilenumber':1,'telephonenumber':0}
r = requests.post(url,data=payload)
print r.content