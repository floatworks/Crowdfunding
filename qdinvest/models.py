#coding:utf-8
from django.db import models


'''
基础用户表
'''
class USERS(models.Model):
	u_name = models.CharField(max_length=50,verbose_name='用户名',unique=True)
	u_pwd = models.CharField(max_length=20,verbose_name='密码')
	u_tel = models.CharField(max_length=20,verbose_name='手机号')
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
	ac_like = models.IntegerField(default=0,verbose_name="关注的项目数")
	ac_support = models.IntegerField(default=0,verbose_name="支持的项目数")
	ac_sponsor = models.IntegerField(default=0,verbose_name="发起的项目数")
	ac_infos = models.IntegerField(default=0,verbose_name="未读消息数量")
	ac_balance = models.DecimalField(max_digits=16,decimal_places=4,verbose_name='账户余额')
	ac_frozen = models.DecimalField(max_digits=16,decimal_places=4,verbose_name='冻结资金')
	ac_soon_profit = models.DecimalField(max_digits=16,decimal_places=4,verbose_name='待收收益')
	ac_actual_profit = models.DecimalField(max_digits=16,decimal_places=4,verbose_name='实际收益')
	ac_total_invest = models.DecimalField(max_digits=16,decimal_places=4,verbose_name='累计投资')
	ac_total_profit = models.DecimalField(max_digits=16,decimal_places=4,verbose_name='累计收益')

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
公司类型 
'''
class PRO_TYPE(models.Model):
	pt_name = models.CharField(max_length=50,verbose_name="公司类型")

	def __unicode__(self):
		return self.pt_name

	class Meta:
		verbose_name = '公司类型'
		verbose_name_plural = '公司类型管理'

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

'''
股权众筹
'''
class STOCK(models.Model):
	st_user = models.ForeignKey(USERS,verbose_name="用户")
	st_title = models.CharField(max_length=100,verbose_name="标题")
	st_image = models.ImageField(upload_to ='upload/logo/',verbose_name="LOGO")
	st_brief = models.CharField(max_length=200,verbose_name="描述")
	st_begin_time = models.DateTimeField(verbose_name="开始时间")
	st_end_time = models.DateTimeField(verbose_name="结束时间")
	st_create_time = models.DateTimeField(verbose_name="创建时间")
	st_scale = models.FloatField(verbose_name="出让比例")
	st_total_price = models.DecimalField(max_digits=16,decimal_places=4,verbose_name='投资总额')
	st_current_price = models.DecimalField(max_digits=16,decimal_places=4,verbose_name='当前已经认购')
	st_min_price = models.DecimalField(max_digits=16,decimal_places=4,verbose_name='认购起点')
	st_industry = models.ForeignKey(INDUSTRY,verbose_name="所属行业")
	st_province = models.ForeignKey(PROVINCE,verbose_name="所属地区")
	st_pro_type = models.ForeignKey(PRO_TYPE,verbose_name="项目属性")
	st_com_type = models.ForeignKey(COM_TYPE,verbose_name="公司类型")
	st_like_count = models.IntegerField(default=0,verbose_name="关注数")
	st_invest_count = models.IntegerField(default=0,verbose_name="认购次数")
	st_hint = models.TextField(verbose_name="重要提示",null=True,blank=True)
	st_com_brief = models.TextField(verbose_name="公司简介",null=True,blank=True)
	st_protect = models.TextField(verbose_name="投资者保护机制",null=True,blank=True)
	st_inf_expose = models.TextField(verbose_name="信息披露安排",null=True,blank=True)
	st_plan = models.TextField(verbose_name="融资计划",null=True,blank=True)
	st_finance = models.TextField(verbose_name="财务情况",null=True,blank=True)
	st_good_bad = models.TextField(verbose_name="优势和劣势",null=True,blank=True)
	st_market = models.TextField(verbose_name="市场分析",null=True,blank=True)
	st_business = models.TextField(verbose_name="商业模式",null=True,blank=True)
	st_risk = models.TextField(verbose_name="风险控制",null=True,blank=True)
	st_team = models.TextField(verbose_name="团队介绍",null=True,blank=True)
	st_prospectus = models.TextField(verbose_name="投资计划书",null=True,blank=True)
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
	bo_com_name = models.CharField(max_length=100,verbose_name="企业名称")
	bo_brief = models.CharField(max_length=200,verbose_name="描述")
	bo_begin_time = models.DateTimeField(verbose_name="开始时间")
	bo_create_time = models.DateTimeField(verbose_name="创建时间")
	bo_end_time = models.DateTimeField(verbose_name="结束时间")
	bo_scale = models.FloatField(verbose_name="年转化率")
	bo_province = models.ForeignKey(PROVINCE,verbose_name="所属地区")
	bo_total_price = models.DecimalField(max_digits=16,decimal_places=4,verbose_name='投资总额')
	bo_current_price = models.DecimalField(max_digits=16,decimal_places=4,verbose_name='当前已经认购')
	bo_min_price = models.DecimalField(max_digits=16,decimal_places=4,verbose_name='认购起点')
	bo_pro_type = models.ForeignKey(PRO_TYPE,verbose_name="项目属性")
	bo_com_type = models.ForeignKey(COM_TYPE,verbose_name="公司类型")
	bo_goal = models.CharField(max_length=200,verbose_name="借款用途")
	bo_repayment = models.CharField(max_length=200,verbose_name="还款来源")
	bo_com_inf = models.TextField(verbose_name="企业信息",null=True,blank=True)
	bo_risk_inf = models.TextField(verbose_name="风险信息",null=True,blank=True)
	bo_files = models.TextField(verbose_name="相关文件",null=True,blank=True)
	bo_repay_plan = models.TextField(verbose_name="还款计划",null=True,blank=True)
	bo_finance = models.TextField(verbose_name="财务计划",null=True,blank=True)
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
用户投资 股权众筹
'''
class INVEST_STOCK(models.Model):
	is_user = models.ForeignKey(USERS,verbose_name="用户")
	is_stock = models.ForeignKey(STOCK,verbose_name="股权众筹")
	is_amount = models.DecimalField(max_digits=16,decimal_places=4,verbose_name="投资金额")
	is_date = models.DateTimeField(verbose_name="投资时间")
	is_soon_profit = models.DecimalField(max_digits=16,decimal_places=4,verbose_name="预计收入")
	is_profit_date = models.DateField(verbose_name="预计收入日期")
	is_status = models.IntegerField(default=0,verbose_name="审核状态")

	def __unicode__(self):
		return self.in_stock.st_title

	class Meta:
		verbose_name = '用户投资股权众筹'
		verbose_name_plural = '用户投资股权众筹'

'''
用户投资 债权众筹 
'''
class INVEST_BOND(models.Model):
	ib_user = models.ForeignKey(USERS,verbose_name="用户")
	ib_bond = models.ForeignKey(BOND,verbose_name="股权众筹")
	ib_amount = models.DecimalField(max_digits=16,decimal_places=4,verbose_name='投资金额')
	ib_date = models.DateTimeField(verbose_name="投资时间")
	ib_soon_profit = models.DecimalField(max_digits=16,decimal_places=4,verbose_name="预计收入")
	ib_profit_date = models.DateField(verbose_name="预计收入日期")
	ib_status = models.IntegerField(default=0,verbose_name="审核状态")

	def __unicode__(self):
		return self.in_stock.st_title

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
	uf_stock = models.ForeignKey(STOCK,verbose_name="股权众筹")
	uf_bond = models.ForeignKey(BOND,verbose_name="股权众筹")
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


'''
系统通知表
'''
class NOTICE(models.Model):
	no_title = models.CharField(max_length=100,verbose_name="通知标题")
	no_body = models.TextField(verbose_name="通知内容")
	no_time = models.DateTimeField(verbose_name="通知时间")
	no_type = models.IntegerField(verbose_name="通知类型",help_text="比如紧急通知，维护通知，广告通知之类")
	no_sort = models.IntegerField(verbose_name="优先级")
	no_is_delete = models.IntegerField(verbose_name="是否删除",default=0,help_text="0 未删除 1 已删除")

	class Meta:
		verbose_name = '系统通知'
		verbose_name_plural = '系统通知管理'

'''
用户通知表
'''
class NOTICE_USER(models.Model):
	nu_title = models.CharField(max_length=100,verbose_name="通知标题")
	nu_body = models.TextField(verbose_name="通知管理")
	nu_time = models.DateTimeField(verbose_name="通知内容")
	nu_user = models.ForeignKey(USERS,verbose_name="用户")
	nu_type = models.IntegerField(verbose_name="通知类型",help_text="比如收益通知，债权众筹提前打款等")
	nu_is_read = models.IntegerField(verbose_name="是否已读",help_text="0 未读 1 已读")
	nu_is_delete = models.IntegerField(verbose_name="是否删除",default=0,help_text="0 未删除 1 已删除")

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
	pr_title = models.CharField(max_length=100,verbose_name="收益项目名称")

	class Meta:
		verbose_name = '用户收益'
		verbose_name_plural = '用户收益管理'

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

