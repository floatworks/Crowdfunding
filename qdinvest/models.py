#coding:utf-8
from django.db import models
from DjangoUeditor.models import UEditorField
from django.conf import settings
from django.contrib.contenttypes.models import ContentType  
from django.contrib.contenttypes import generic  
from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from django.db.models import Sum
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

import simplejson as json
import push as P
#from django.core.signals import post_save

'''
基础用户表
'''
class USERS(models.Model):
	u_name = models.CharField(max_length=50,verbose_name='用户名',unique=True)
	u_pwd = models.CharField(max_length=20,verbose_name='密码')
	u_tel = models.CharField(max_length=20,verbose_name='手机号',unique=True)
	u_status = models.IntegerField(default=0,verbose_name='用户状态',help_text='0 正常')

	def __unicode__(self):
		return self.u_name

	class Meta:
		verbose_name = '用户'
		verbose_name_plural = '用户管理'

'''
用户账户信息
'''
class ACCOUNT(models.Model):
	ac_user = models.OneToOneField(USERS,verbose_name="用户")
	ac_like = models.IntegerField(default=0,verbose_name="关注项目数")
	ac_support = models.IntegerField(default=0,verbose_name="支持项目数")
	ac_sponsor = models.IntegerField(default=0,verbose_name="发起项目数")
	ac_infos = models.IntegerField(default=0,verbose_name="未读消息数")
	#ac_balance = models.DecimalField(max_digits=16,decimal_places=4,verbose_name='账户余额')
	#ac_frozen = models.DecimalField(max_digits=16,decimal_places=4,verbose_name='冻结资金')
	#ac_soon_profit = models.DecimalField(max_digits=16,decimal_places=4,verbose_name='待收收益')
	#ac_actual_profit = models.DecimalField(max_digits=16,decimal_places=4,verbose_name='实际收益')
	ac_stock_invest = models.DecimalField(max_digits=16,decimal_places=4,verbose_name='股权投资')
	ac_bond_invest = models.DecimalField(max_digits=16,decimal_places=4,verbose_name='债权投资')
	ac_total_invest = models.DecimalField(max_digits=16,decimal_places=4,verbose_name='投资总额')
	ac_stock_profit = models.DecimalField(max_digits=16,decimal_places=4,verbose_name='股权收益')
	ac_bond_profit = models.DecimalField(max_digits=16,decimal_places=4,verbose_name='债权收益')
	ac_total_profit = models.DecimalField(max_digits=16,decimal_places=4,verbose_name='收益总额')
	ac_subscription = models.DecimalField(max_digits=16,decimal_places=4,verbose_name='认购定金')
	ac_total_subscription = models.DecimalField(max_digits=16,decimal_places=4,verbose_name='认购总额')

	def __unicode__(self):
		return self.ac_user.u_name

	class Meta:
		verbose_name = '账户'
		verbose_name_plural = '账户管理'

'''
行业
'''
class INDUSTRY(models.Model):
	in_name = models.CharField(max_length=100,verbose_name="行业名称")
	in_sort = models.IntegerField(default=0,verbose_name="排序")

	def __unicode__(self):
		return self.in_name

	class Meta:
		verbose_name = '行业'
		verbose_name_plural = '行业管理'

'''
地区 城市 基础信息
'''
class PROVINCE(models.Model):
	pr_name = models.CharField(max_length=20,verbose_name="省")

	def __unicode__(self):
		return self.pr_name

	class Meta:
		verbose_name = '地区'
		verbose_name_plural = '地区管理'

'''
项目属性 
'''
class PRO_TYPE(models.Model):
	pt_name = models.CharField(max_length=50,verbose_name="项目属性")

	def __unicode__(self):
		return self.pt_name

	class Meta:
		verbose_name = '项目属性'
		verbose_name_plural = '项目属性管理'

'''
企业类型 
'''
class COM_TYPE(models.Model):
	ct_name = models.CharField(max_length=50,verbose_name="公司类型")

	def __unicode__(self):
		return self.ct_name

	class Meta:
		verbose_name = '企业类型'
		verbose_name_plural = '企业类型管理'

RECOMMEND_STATUS =(
	(0,u'不推荐'),
	(1,u'推荐'),
	)

'''
股权众筹
'''
class STOCK(models.Model):
	st_user = models.ForeignKey(USERS,verbose_name="用户")
	st_title = models.CharField(max_length=100,verbose_name="标题")
	st_code = models.CharField(max_length=30,verbose_name="股份代码")
	st_per_price = models.DecimalField(max_digits=16,decimal_places=4,verbose_name='每股认购价格')
	#st_image = models.ImageField(upload_to ='logo/',verbose_name="详细页大图")
	st_image = ProcessedImageField(upload_to ='logo/',verbose_name='详细页大图',help_text='320px*160px为宜，图像大小不宜超过200KB',
					processors=[ResizeToFill(320, 160)],format='JPEG')
	st_logo = ProcessedImageField(upload_to ='logo_100x100/',verbose_name='列表页图标',help_text='100px*100px为宜，图像大小不宜超过50KB',
					processors=[ResizeToFill(100, 100)],format='JPEG')
	st_video = models.CharField(max_length=100,verbose_name="保利威视视频id",null=True,blank=True)
	st_brief = models.CharField(max_length=200,verbose_name="描述")
	st_begin_time = models.DateTimeField(verbose_name="开始时间")
	st_end_time = models.DateTimeField(verbose_name="结束时间")
	st_create_time = models.DateTimeField(verbose_name="创建时间")
	st_is_commend = models.IntegerField(verbose_name="是否推荐",default=0,choices=RECOMMEND_STATUS)
	st_scale = models.FloatField(verbose_name="出让比例")
	st_total_price = models.DecimalField(max_digits=16,decimal_places=4,verbose_name='投资总额')
	st_current_price = models.DecimalField(max_digits=16,decimal_places=4,verbose_name='当前已经认购')
	st_min_price = models.DecimalField(max_digits=16,decimal_places=4,verbose_name='认购起点')
	st_industry = models.ForeignKey(INDUSTRY,verbose_name="所属行业")
	st_province = models.ForeignKey(PROVINCE,verbose_name="所属地区")
	st_pro_type = models.ForeignKey(PRO_TYPE,verbose_name="项目属性")
	st_com_type = models.ForeignKey(COM_TYPE,verbose_name="公司类型")
	st_like_count = models.IntegerField(default=0,verbose_name="关注数")
	st_view_count = models.IntegerField(default=0,verbose_name="点击数")
	st_invest_count = models.IntegerField(default=0,verbose_name="认购次数")
	st_hint = UEditorField(verbose_name='重要提示',imagePath="ueditor/images/",
        filePath="ueditor/files/",settings=settings.UEDITOR_SETTINGS['config'],
		upload_settings={'imageMaxSize':2048000},null=True,blank=True)
	st_com_brief = UEditorField(verbose_name="公司简介",imagePath="ueditor/images/",
        filePath="ueditor/files/",settings=settings.UEDITOR_SETTINGS['config'],
		upload_settings={'imageMaxSize':2048000},null=True,blank=True)
	st_protect = UEditorField(verbose_name="投资者保护机制",imagePath="ueditor/images/",
        filePath="ueditor/files/",settings=settings.UEDITOR_SETTINGS['config'],
		upload_settings={'imageMaxSize':2048000},null=True,blank=True)
	st_inf_expose = UEditorField(verbose_name="信息披露安排",imagePath="ueditor/images/",
        filePath="ueditor/files/",settings=settings.UEDITOR_SETTINGS['config'],
		upload_settings={'imageMaxSize':2048000},null=True,blank=True)
	st_plan = UEditorField(verbose_name="融资计划",imagePath="ueditor/images/",
        filePath="ueditor/files/",settings=settings.UEDITOR_SETTINGS['config'],
		upload_settings={'imageMaxSize':2048000},null=True,blank=True)
	#st_good_bad = UEditorField(verbose_name="优势和劣势",imagePath="ueditor/images/",
    #    filePath="ueditor/files/",settings=settings.UEDITOR_SETTINGS['config'],
	#	upload_settings={'imageMaxSize':2048000},null=True,blank=True)
	st_business = UEditorField(verbose_name="商业模式",imagePath="ueditor/images/",
        filePath="ueditor/files/",settings=settings.UEDITOR_SETTINGS['config'],
		upload_settings={'imageMaxSize':2048000},null=True,blank=True)
	st_market = UEditorField(verbose_name="业务发展",imagePath="ueditor/images/",
        filePath="ueditor/files/",settings=settings.UEDITOR_SETTINGS['config'],
		upload_settings={'imageMaxSize':2048000},null=True,blank=True)
	st_finance = UEditorField(verbose_name="财务数据",imagePath="ueditor/images/",
        filePath="ueditor/files/",settings=settings.UEDITOR_SETTINGS['config'],
		upload_settings={'imageMaxSize':2048000},null=True,blank=True)
	st_risk = UEditorField(verbose_name="募集资金投向",imagePath="ueditor/images/",
        filePath="ueditor/files/",settings=settings.UEDITOR_SETTINGS['config'],
		upload_settings={'imageMaxSize':2048000},null=True,blank=True)
	st_team = UEditorField(verbose_name="团队介绍",imagePath="ueditor/images/",
        filePath="ueditor/files/",settings=settings.UEDITOR_SETTINGS['config'],
		upload_settings={'imageMaxSize':2048000},null=True,blank=True)
	st_prospectus = UEditorField(verbose_name="投资计划书",imagePath="ueditor/images/",
        filePath="ueditor/files/",settings=settings.UEDITOR_SETTINGS['config'],
		upload_settings={'imageMaxSize':2048000},null=True,blank=True)
	st_manage = UEditorField(verbose_name="投后管理",imagePath="ueditor/images/",
        filePath="ueditor/files/",settings=settings.UEDITOR_SETTINGS['config'],
		upload_settings={'imageMaxSize':2048000},null=True,blank=True)
	st_sort = models.IntegerField(default=0,verbose_name="排序")
	st_status = models.IntegerField(default=0,verbose_name="状态")

	def __unicode__(self):
		return self.st_title

	class Meta:
		verbose_name = '股权众筹'
		verbose_name_plural = '股权众筹管理'

'''
债权众筹 
'''
class BOND(models.Model):
	bo_user = models.ForeignKey(USERS,verbose_name="用户")
	bo_title = models.CharField(max_length=100,verbose_name="标题")
	bo_code = models.CharField(max_length=30,verbose_name="股份代码")
	#bo_image = models.ImageField(upload_to ='logo/',verbose_name="LOGO")
	bo_image = ProcessedImageField(upload_to ='logo/',verbose_name='详细页大图',help_text='320px*160px为宜，图像大小不宜超过200KB',
					processors=[ResizeToFill(320, 160)],format='JPEG')
	bo_logo = ProcessedImageField(upload_to ='logo_100x100/',verbose_name='列表页图标',help_text='100px*100px为宜，图像大小不宜超过50KB',
					processors=[ResizeToFill(100, 100)],format='JPEG')
	bo_video = models.CharField(max_length=100,verbose_name="保利威视视频id",null=True,blank=True)
	bo_com_name = models.CharField(max_length=100,verbose_name="企业名称")
	bo_brief = models.CharField(max_length=200,verbose_name="经营用途")
	bo_begin_time = models.DateTimeField(verbose_name="开始时间")
	bo_create_time = models.DateTimeField(verbose_name="创建时间")
	bo_end_time = models.DateTimeField(verbose_name="结束时间")
	bo_is_commend = models.IntegerField(verbose_name="是否推荐",default=0,choices=RECOMMEND_STATUS)
	bo_scale = models.FloatField(verbose_name="年转化率",help_text="单位:%")
	bo_province = models.ForeignKey(PROVINCE,verbose_name="所属地区")
	bo_industry = models.ForeignKey(INDUSTRY,verbose_name="所属行业")
	bo_total_price = models.DecimalField(max_digits=16,decimal_places=4,verbose_name='融资总额')
	bo_current_price = models.DecimalField(max_digits=16,decimal_places=4,verbose_name='当前已经认购')
	bo_min_price = models.DecimalField(max_digits=16,decimal_places=4,verbose_name='认购起点')
	bo_pro_type = models.ForeignKey(PRO_TYPE,verbose_name="项目属性")
	bo_com_type = models.ForeignKey(COM_TYPE,verbose_name="公司类型")
	bo_like_count = models.IntegerField(default=0,verbose_name="关注数")
	bo_view_count = models.IntegerField(default=0,verbose_name="点击数")
	bo_invest_count = models.IntegerField(default=0,verbose_name="认购次数")
	bo_goal = models.CharField(max_length=200,verbose_name="借款用途")
	bo_repayment = models.CharField(max_length=200,verbose_name="还款来源")
	bo_com_inf = UEditorField(verbose_name="企业信息",imagePath="ueditor/images/",
        filePath="ueditor/files/",settings=settings.UEDITOR_SETTINGS['config'],
		upload_settings={'imageMaxSize':2048000},null=True,blank=True)
	bo_risk_inf = UEditorField(verbose_name="风险信息",imagePath="ueditor/images/",
        filePath="ueditor/files/",settings=settings.UEDITOR_SETTINGS['config'],
		upload_settings={'imageMaxSize':2048000},null=True,blank=True)
	bo_files = UEditorField(verbose_name="相关文件",imagePath="ueditor/images/",
        filePath="ueditor/files/",settings=settings.UEDITOR_SETTINGS['config'],
		upload_settings={'imageMaxSize':2048000},null=True,blank=True)
	bo_repay_plan = UEditorField(verbose_name="还款计划",imagePath="ueditor/images/",
        filePath="ueditor/files/",settings=settings.UEDITOR_SETTINGS['config'],
		upload_settings={'imageMaxSize':2048000},null=True,blank=True)
	bo_finance = UEditorField(verbose_name="财务计划",imagePath="ueditor/images/",
        filePath="ueditor/files/",settings=settings.UEDITOR_SETTINGS['config'],
		upload_settings={'imageMaxSize':2048000},null=True,blank=True)
	bo_manage = UEditorField(verbose_name="投后管理",imagePath="ueditor/images/",
        filePath="ueditor/files/",settings=settings.UEDITOR_SETTINGS['config'],
		upload_settings={'imageMaxSize':2048000},null=True,blank=True)
	bo_sort = models.IntegerField(default=0,verbose_name="排序")
	bo_status = models.IntegerField(default=0,verbose_name="状态")

	def __unicode__(self):
		return self.bo_title

	class Meta:
		verbose_name = '债权众筹'
		verbose_name_plural = '债权众筹管理'


'''
众筹转让
'''

'''
用户投资状态说明,不可修改
'''
class INVEST_STATUS(models.Model):
	status = models.CharField(max_length=20,verbose_name='状态')
	sort = models.IntegerField(default=0,verbose_name='排序')

	def __unicode__(self):
		return self.status

	class Meta:
		verbose_name = '认购状态'
		verbose_name_plural = '认购状态'

'''
用户投资 股权众筹
'''
class INVEST_STOCK(models.Model):
	is_user = models.ForeignKey(USERS,verbose_name="用户")
	is_stock = models.ForeignKey(STOCK,verbose_name="股权众筹")
	is_amount = models.DecimalField(max_digits=16,decimal_places=4,verbose_name="投资金额")
	is_date = models.DateTimeField(verbose_name="投资时间")
	is_soon_profit = models.DecimalField(max_digits=16,decimal_places=4,verbose_name="预计收入",null=True)
	is_profit_date = models.DateField(verbose_name="预计收入日期",null=True)
	#is_status = models.IntegerField(default=0,verbose_name="审核状态",help_text="0:认购中 1:持有中 2:已完成")
	is_status = models.ForeignKey(INVEST_STATUS,verbose_name='审核状态')

	def __unicode__(self):
		return self.is_stock.st_title

	class Meta:
		verbose_name = '用户投资股权众筹'
		verbose_name_plural = '用户投资股权众筹'

'''
用户投资 债权众筹 
'''
class INVEST_BOND(models.Model):
	ib_user = models.ForeignKey(USERS,verbose_name="用户")
	ib_bond = models.ForeignKey(BOND,verbose_name="债权众筹")
	ib_amount = models.DecimalField(max_digits=16,decimal_places=4,verbose_name='投资金额')
	ib_date = models.DateTimeField(verbose_name="投资时间")
	ib_soon_profit = models.DecimalField(max_digits=16,decimal_places=4,verbose_name="预计收入",null=True)
	ib_profit_date = models.DateField(verbose_name="预计收入日期",null=True)
	#ib_status = models.IntegerField(default=0,verbose_name="审核状态",help_text="0:认购中 1:持有中 2:已完成")
	ib_status = models.ForeignKey(INVEST_STATUS,verbose_name='审核状态')

	def __unicode__(self):
		return self.ib_bond.bo_title

	class Meta:
		verbose_name = '用户投资债权众筹'
		verbose_name_plural = '用户投资债权众筹'

'''
用户充值
'''
class RECHARGE(models.Model):
	rc_user = models.ForeignKey(USERS,verbose_name="用户")
	rc_type = models.IntegerField(default=0,verbose_name="操作类型",help_text="0充值，1提现")
	rc_value = models.DecimalField(max_digits=16,decimal_places=4,verbose_name='金额')
	rc_date = models.DateTimeField(verbose_name='操作时间')
	rc_status = models.IntegerField(default=0,verbose_name="状态")

	def __unicode__(self):
		return self.ac_user.u_name

	class Meta:
		verbose_name = '充值信息'
		verbose_name_plural = '充值管理'

'''
用户喜欢
'''
class USER_FOCUS(models.Model):
	uf_user	= models.ForeignKey(USERS,verbose_name="用户")
	uf_stock = models.ForeignKey(STOCK,verbose_name="股权众筹",null=True,blank=True)
	uf_bond = models.ForeignKey(BOND,verbose_name="股权众筹",null=True,blank=True)
	uf_update_time = models.DateTimeField(verbose_name="更新时间")

	class Meta:
		verbose_name = '关注'
		verbose_name_plural = '关注记录'

'''
用户讨论
'''
class TALK(models.Model):
	ta_user = models.ForeignKey(USERS,verbose_name="用户")
	ta_stock = models.ForeignKey(STOCK,verbose_name="股权众筹")
	ta_msg = models.CharField(max_length=500,verbose_name="评论内容")
	ta_pre_id = models.IntegerField(default=0,verbose_name="父ID")

	class Meta:
		verbose_name = '用户讨论'
		verbose_name_plural = '股权众筹用户讨论记录'

NOTICES_STATUS = (
	(0, u"未删除"),
    (1, u"已删除"),
	)
NOTICES_TYPE = (
	(0, u"紧急通知"),
    (1, u"维护通知"),
    (2, u"推广通知"),
    (3, u"广告"),
	)

'''
系统通知表
'''
class NOTICE(models.Model):
	no_title = models.CharField(max_length=100,verbose_name="通知标题")
	no_brief = models.CharField(max_length=200,verbose_name="通知概要",help_text="请不要超过100个汉字")
	no_body = UEditorField(verbose_name="通知内容",imagePath="ueditor/images/",
        filePath="ueditor/files/",settings=settings.UEDITOR_SETTINGS['config'],
		upload_settings={'imageMaxSize':2048000})
	no_time = models.DateTimeField(verbose_name="通知时间")
	no_type = models.IntegerField(verbose_name="通知类型",choices=NOTICES_TYPE)
	no_sort = models.IntegerField(verbose_name="优先级")
	no_is_delete = models.IntegerField(verbose_name="是否删除",default=0,choices=NOTICES_STATUS)

	def __unicode__(self):
		return self.no_title

	class Meta:
		verbose_name = '系统通知'
		verbose_name_plural = '系统通知管理'

NOTICE_USER_IS_READ = (
	(0, u"未读"),
    (1, u"已读"),
	)
NOTICES_USER_TYPE = (
	(0, u"收益通知"),
    (1, u"其他"),
	)

'''
用户通知表
'''
class NOTICE_USER(models.Model):
	nu_title = models.CharField(max_length=100,verbose_name="通知标题")
	nu_brief = models.CharField(max_length=200,verbose_name="通知概要",help_text="请不要超过100个汉字")
	nu_body = UEditorField(verbose_name="通知内容",imagePath="ueditor/images/",
        filePath="ueditor/files/",settings=settings.UEDITOR_SETTINGS['config'],
		upload_settings={'imageMaxSize':2048000})
	nu_time = models.DateTimeField(verbose_name="通知时间")
	nu_user = models.ForeignKey(USERS,verbose_name="用户")
	nu_type = models.IntegerField(verbose_name="通知类型",choices=NOTICES_USER_TYPE)
	nu_is_read = models.IntegerField(verbose_name="是否已读",default=0,choices=NOTICE_USER_IS_READ)
	nu_is_delete = models.IntegerField(verbose_name="是否删除",default=0,choices=NOTICES_STATUS)

	def __unicode__(self):
		return self.nu_title

	class Meta:
		verbose_name = '用户通知'
		verbose_name_plural = '用户通知管理'''

'''
系统通知查看
'''
class NOTICE_READ(models.Model):
	nr_user = models.ForeignKey(USERS,verbose_name="用户")
	nr_notice = models.ForeignKey(NOTICE,verbose_name="系统通知")

	class Meta:
		verbose_name = '系统通知查看'
		verbose_name_plural = '系统通知是否已读'


'''
用户收益表
'''
class PROFIT(models.Model):
	pr_user = models.ForeignKey(USERS,verbose_name="用户")
	pr_amount = models.DecimalField(max_digits=16,decimal_places=4,verbose_name='收益金额')
	pr_date = models.DateField(verbose_name="收益时间")
	pr_stock = models.ForeignKey(STOCK,verbose_name="股权众筹",null=True,blank=True,help_text="二选一即可")
	pr_bond = models.ForeignKey(BOND,verbose_name="债权众筹",null=True,blank=True,help_text="二选一即可")

	def __unicode__(self):
		return self.pr_user.u_name+'的收益'

	class Meta:
		verbose_name = '用户收益'
		verbose_name_plural = '用户收益管理'

PAYMENT_STATUS = (
	(0, u"已支付"),
    (1, u"已退还"),
	)

'''
用户定金表
'''
class PAYMENT(models.Model):
	pa_user = models.ForeignKey(USERS,verbose_name="用户")
	pa_amount = models.DecimalField(max_digits=16,decimal_places=4,verbose_name='定金数额')
	pa_date = models.DateTimeField(verbose_name="支付时间")
	pa_stock = models.ForeignKey(STOCK,verbose_name="股权众筹",null=True,blank=True,help_text="二选一即可")
	pa_bond = models.ForeignKey(BOND,verbose_name="债权众筹",null=True,blank=True,help_text="二选一即可")
	pa_status = models.SmallIntegerField(default=0,verbose_name="状态",choices=PAYMENT_STATUS)

	class Meta:
		verbose_name = '定金'
		verbose_name_plural = '定金管理'

'''
随机验证码
'''
class RANDOMCODE(models.Model):
	rc_tel = models.CharField(max_length=20,verbose_name='手机号码')
	rc_code = models.CharField(max_length=10,verbose_name='验证码')
	rc_time = models.DateTimeField(verbose_name='更新时间')

	def __unicode__(self):
		return self.rc_tel

	class Meta:
		verbose_name = '验证码'
		verbose_name_plural = '验证码管理'

'''
token合法性验证
'''
class TOKEN(models.Model):
	t_user = models.ForeignKey(USERS,verbose_name='用户')
	t_token = models.CharField(max_length=50,verbose_name='token')
	t_time = models.DateTimeField(verbose_name='更新时间')

	def __unicode__(self):
		return self.t_user.u_name

	class Meta:
		verbose_name = 'token'
		verbose_name_plural = 'TOKEN管理'

'''
系统基础参数
'''
class SETTINGS(models.Model):
	se_android_version = models.CharField(max_length=20,verbose_name='Android版本')
	se_ios_version = models.CharField(max_length=20,verbose_name='IOS版本')

	def __unicode__(self):
		return self.se_android_version

	class Meta:
		verbose_name = '系统基础参数'
		verbose_name_plural = '系统基础参数管理'

'''
用户反馈表
'''
class FEEDBACK(models.Model):
	fe_user = models.ForeignKey(USERS,verbose_name='用户')
	fe_mail = models.CharField(max_length=100,verbose_name='邮件地址',null=True,blank=True)
	fe_time = models.DateTimeField(verbose_name='时间')
	fe_content = models.CharField(max_length=500,verbose_name='反馈内容')

	def __unicode__(self):
		return self.fe_user.u_name

	class Meta:
		verbose_name = '用户反馈'
		verbose_name_plural = '用户反馈管理'

'''
协议数据
'''
class PROTOCOL(models.Model):
	pr_instructions = UEditorField(verbose_name='清大众筹用户服务协议',imagePath="ueditor/images/",
        filePath="ueditor/files/",settings=settings.UEDITOR_SETTINGS['config'],
		upload_settings={'imageMaxSize':2048000},null=True,blank=True)
	pr_investor = UEditorField(verbose_name='投资者必读',imagePath="ueditor/images/",
        filePath="ueditor/files/",settings=settings.UEDITOR_SETTINGS['config'],
		upload_settings={'imageMaxSize':2048000},null=True,blank=True)
	pr_version = models.IntegerField(verbose_name="版本",help_text="整形，将已最新版本为准")
	pr_date = models.DateTimeField(verbose_name="更新时间")

	def __unicode__(self):
		return self.pr_version

	class Meta:
		verbose_name = '用户协议'
		verbose_name_plural = '用户协议管理'

'''
定义各类触发函数
'''

'''
股权认购触发函数
'''
@receiver(post_save, sender=INVEST_STOCK, dispatch_uid="unique_invest_stock")
def invest_stock_callback(sender, instance, signal, *args, **kwargs):
	post_data = instance
	ACCOUNT_obj = ACCOUNT.objects.get(ac_user__exact = post_data.is_user)
	#重新计算该账户总的认购金额
	ac_total_stock =  SUMModel(INVEST_STOCK,{'is_user':post_data.is_user},'is_amount')
	ac_total_bond =  SUMModel(INVEST_BOND,{'ib_user':post_data.is_user},'ib_amount')
	ACCOUNT_obj.ac_total_subscription = str(ac_total_stock+ac_total_bond)
	invest_stock = SUMModel(INVEST_STOCK,{'is_user':post_data.is_user,'is_status__id':2},'is_amount')
	invest_stock_3 = SUMModel(INVEST_STOCK,{'is_user':post_data.is_user,'is_status__id':3},'is_amount')
	invest_bond = SUMModel(INVEST_BOND,{'ib_user':post_data.is_user,'ib_status__id':2},'ib_amount')
	invest_bond_3 = SUMModel(INVEST_BOND,{'ib_user':post_data.is_user,'ib_status__id':3},'ib_amount')
	ACCOUNT_obj.ac_stock_invest = str(invest_stock+invest_stock_3)
	ACCOUNT_obj.ac_bond_invest = str(invest_bond+invest_bond_3)
	ACCOUNT_obj.ac_total_invest = str(invest_stock+invest_stock_3+invest_bond+invest_bond_3)
	ACCOUNT_obj.save()

	#修改当前项目已经认购的金额
	STOCK_obj = post_data.is_stock
	st_current_price = SUMModel(INVEST_STOCK,{'is_status__id':2},'is_amount') + SUMModel(INVEST_STOCK,{'is_status__id':3},'is_amount')
	STOCK_obj.st_current_price = str(st_current_price)
	STOCK_obj.save()

'''
债权认购触发函数
'''
@receiver(post_save, sender=INVEST_BOND, dispatch_uid="unique_invest_bond")
def invest_bond_callback(sender, instance, signal, *args, **kwargs):
	post_data = instance
	ACCOUNT_obj = ACCOUNT.objects.get(ac_user__exact = post_data.ib_user)
	#重新计算该账户总的认购金额
	ac_total_stock =  SUMModel(INVEST_STOCK,{'is_user':post_data.ib_user},'is_amount')
	ac_total_bond =  SUMModel(INVEST_BOND,{'ib_user':post_data.ib_user},'ib_amount')
	ACCOUNT_obj.ac_total_subscription = str(ac_total_stock+ac_total_bond)
	invest_stock = SUMModel(INVEST_STOCK,{'is_user':post_data.ib_user,'is_status__id':2},'is_amount')
	invest_stock_3 = SUMModel(INVEST_STOCK,{'is_user':post_data.ib_user,'is_status__id':3},'is_amount')
	invest_bond = SUMModel(INVEST_BOND,{'ib_user':post_data.ib_user,'ib_status__id':2},'ib_amount')
	invest_bond_3 = SUMModel(INVEST_BOND,{'ib_user':post_data.ib_user,'ib_status__id':3},'ib_amount')
	ACCOUNT_obj.ac_stock_invest = str(invest_stock+invest_stock_3)
	ACCOUNT_obj.ac_bond_invest = str(invest_bond+invest_bond_3)
	ACCOUNT_obj.ac_total_invest = str(invest_stock+invest_stock_3+invest_bond+invest_bond_3)
	ACCOUNT_obj.save()

	#修改当前项目已经认购的金额
	BOND_obj = post_data.ib_bond
	bo_current_price = SUMModel(INVEST_BOND,{'ib_status__id':2},'ib_amount') + SUMModel(INVEST_BOND,{'ib_status__id':3},'ib_amount')
	BOND_obj.bo_current_price = str(bo_current_price)
	BOND_obj.save()

'''
收益更改触发函数
'''
def profit_callback(sender, instance, signal, *args, **kwargs):
	post_data = instance
	ACCOUNT_obj = ACCOUNT.objects.get(ac_user__exact = post_data.pr_user)
	#计算收益
	ac_stock_profit = SUMModel(PROFIT,{'pr_user':post_data.pr_user,'pr_bond':None},'pr_amount')
	ac_total_profit = SUMModel(PROFIT,{'pr_user':post_data.pr_user},'pr_amount')
	ACCOUNT_obj.ac_stock_profit = str(ac_stock_profit)
	ACCOUNT_obj.ac_bond_profit = str(ac_total_profit - ac_stock_profit)
	ACCOUNT_obj.ac_total_profit = str(ac_total_profit)
	ACCOUNT_obj.save()

'''
定金更改触发函数
'''
def payment_callback(sender, instance, signal, *args, **kwargs):
	post_data = instance
	ACCOUNT_obj = ACCOUNT.objects.get(ac_user__exact = post_data.pa_user)
	ac_subscription = SUMModel(PAYMENT,{'pa_user':post_data.pa_user,'pa_status':0},'pa_amount')
	ACCOUNT_obj.ac_subscription = str(ac_subscription)
	ACCOUNT_obj.save()

'''
系统消息触发函数
'''
def notice_callback(sender, instance, signal, *args, **kwargs):
	#no_brief = instance.no_brief
	#调用推送接口，推送系统通知
	if kwargs['created']:
		P.PushMessage(alert=instance.no_brief,title=instance.no_title,n_type='sys',n_id=instance.id)
		#增加系统消息，所有人的未读消息数量增加1
		ACCOUNT_objs = ACCOUNT.objects.all()
		for ACCOUNT_obj in ACCOUNT_objs:
			print ACCOUNT_obj
			ACCOUNT_obj.ac_infos += 1
			ACCOUNT_obj.save()

'''
用户消息触发函数
'''
def notice_user_callback(sender, instance, signal, *args, **kwargs):
	if kwargs['created']:
		P.PushMessageUser(alert=instance.nu_brief,title=instance.nu_title,n_type='user',n_id=instance.id,user=instance.nu_user.u_name)
		ACCOUNT_obj = ACCOUNT.objects.get(ac_user=instance.nu_user)
		ACCOUNT_obj.ac_infos += 1
		ACCOUNT_obj.save()

'''
用户表触发函数
'''
def users_callback(sender, instance, signal, *args, **kwargs):
	if kwargs['created']:
		#创建用户的时候同时需要创建用户账户
		ac_infos = NOTICE.objects.filter(no_is_delete = 0).count()
		ACCOUNT_new = ACCOUNT(ac_user=instance,ac_like=0,ac_support=0,ac_sponsor=0,ac_infos=ac_infos,
					ac_stock_invest=0,ac_bond_invest=0,ac_total_invest=0,ac_stock_profit=0,ac_bond_profit=0,
					ac_total_profit=0,ac_subscription=0,ac_total_subscription=0)
		ACCOUNT_new.save()

post_save.connect(invest_stock_callback, sender=INVEST_STOCK,dispatch_uid="unique_invest_stock")
post_delete.connect(invest_stock_callback, sender=INVEST_STOCK,dispatch_uid="unique_invest_stock")
post_save.connect(invest_bond_callback, sender=INVEST_BOND,dispatch_uid="unique_invest_bond")
post_delete.connect(invest_bond_callback, sender=INVEST_BOND,dispatch_uid="unique_invest_bond")

post_save.connect(profit_callback, sender=PROFIT,dispatch_uid="unique_profit")
post_delete.connect(profit_callback, sender=PROFIT,dispatch_uid="unique_profit")

post_save.connect(payment_callback, sender=PAYMENT,dispatch_uid="unique_payment")
post_delete.connect(payment_callback, sender=PAYMENT,dispatch_uid="unique_payment")

post_save.connect(notice_callback,sender=NOTICE,dispatch_uid="unique_notice")

post_save.connect(notice_user_callback,sender=NOTICE_USER,dispatch_uid="unique_notice_user")

post_save.connect(users_callback,sender=USERS,dispatch_uid="unique_users")

#功能类，返回某一张表某个参数的SUM
#kwargs 条件
#object SUM对象
def SUMModel(model,kwargs,object):
	modelSUM =  model.objects.filter(**kwargs).aggregate(Sum(object))[object+'__sum']
	if modelSUM:
		return float(modelSUM)
	else:
		return 0
