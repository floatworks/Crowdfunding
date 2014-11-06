#coding:utf-8
import os
os.environ['DJANGO_SETTINGS_MODULE'] = "Crowdfunding.settings"
import requests
import qdinvest.tools as T
from xml.etree import ElementTree
import re

'''
url = 'http://www.duanxin10086.com/sms.aspx'
code = T.RandCode()
content = '【清大众筹】您的验证码为'+code+'。工作人员不会向您索要，请勿向任何人泄漏。'
payload = {'userid':'7685','account':'tb2014','password':'123456','mobile':'13136652521',
						'content':content,'sendTime':'','action':'send','checkcontent':0,
						'taskName':'','countnumber':1,'mobilenumber':1,'telephonenumber':0}
r = requests.post(url,data=payload)
print r.content
'''

string = '''<?xml version="1.0" encoding="utf-8"?>
<ROOT xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns="JobSendedDescription">
  <RetCode>Sucess</RetCode>
  <JobID>139377527</JobID>
  <OKPhoneCounts>1</OKPhoneCounts>
  <StockReduced>1</StockReduced>
  <ErrPhones />
</ROOT>'''

print string
s = re.search('<RetCode>(?P<status>\w+)</RetCode>',string)
print s.groupdict()['status']