from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

HTTP_CHOICE = (
    ('HTTP', 'HTTP'),
    ('HTTPS', 'HTTPS')
)

REQUEST_TYPE_CHOICE = (
    ('POST', 'POST'),
    ('GET', 'GET'),
    ('PUT', 'PUT'),
    ('DELETE', 'DELETE')
)

REQUEST_PARAMETER_TYPE_CHOICE = (
    ('form-data', '表单(form-data)'),
    ('raw', '源数据(raw)'),
    ('Restful', 'Restful')
)

PARAMETER_TYPE_CHOICE = (
    ('text', 'text'),
    ('file', 'file')
)

HTTP_CODE_CHOICE = (
    ('200', '200'),
    ('404', '404'),
    ('400', '400'),
    ('502', '502'),
    ('500', '500'),
    ('302', '302'),
)
#down下的代码
# EXAMINE_TYPE_CHOICE = (
#     ('no_check', '不校验'),
#     ('only_check_status', '校验http状态'),
#     ('json', 'JSON校验'),
#     ('entirely_check', '完全校验'),
#     ('Regular_check', '正则校验'),
# )

"""
项目转换 modify by gaojingyu  20201218
"""
# 断言类型
EXAMINE_TYPE_CHOICE = (
    ('assertEqual', '等于'),
    ('assertNotEqual', '不等于'),
    ('assertRegexpMatches', '包含'),
    ('assertNotRegexpMatches', '不包含'),
    ('assertGreater', '大于'),
    ('assertGreaterEqual', '大于等于'),
    ('assertLess', '小于'),
    ('assertLessEqual', '小于等于'),
    ('assertIn', '在列表中'),
    ('assertNotIn', '不在列表中'),
)

# 删除标志
Delete_Flag = (
    ('0', '不删除'),
    ('1', '删除')
)

#用例分类
Case_Type_CHOICE = (
    ('0', '数据校验'),
    ('1', '业务逻辑'),
    ('2', '疏通测试')
)

#校验分类
Check_Type_CHOICE = (
    ('0', 'Response校验'),
    ('1', '数据库校验'),

)

PARAM_TYPE = (
    ('0', 'string'),
    ('1', 'datatime'),
    ('2', 'int'),
    ('3', 'list'),

)


# 执行条件
Action_Condition_CHOICE = (
    ('0', 'or'),
    ('1', 'and'),

)


# 认证
authentication = (
    ('0', '无认证'),
    ('1', '加密解密'),
)

# 依赖
relation = (
    ('0', '无依赖'),
    ('1', '有依赖关系'),
)


#随机数
Random_Number = (
    ('0', '无随机数'),
    ('1', '自动生成随机数'),
)

# 随机数类型
Random_Number_Type = (
    ('0', '自动生成10位随机数'),
    ('1', '自动生成姓名'),
    ('2', 'idcard'),
)








UNIT_CHOICE = (
    ('m', '分'),
    ('h', '时'),
    ('d', '天'),
    ('w', '周'),
)

RESULT_CHOICE = (
    ('PASS', '成功'),
    ('FAIL', '失败'),
)

TASK_CHOICE = (
    ('circulation', '循环'),
    ('timing', '定时'),
)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


# ==================扩展用户====================================
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='用户', related_name='user')
    phone = models.CharField(max_length=11, default='无', blank=True, verbose_name='手机号')
    openId = models.CharField(max_length=50, default=0, verbose_name="唯一标识")
    unionid = models.CharField(max_length=50, default=0, verbose_name="企业内唯一标识")

    def __unicode__(self):
        return self.user.username

    def __str__(self):
        return self.phone


class Project(models.Model):
    """
    项目表
    """
    ProjectType = (
        ('Web', 'Web'),
        ('App', 'App')
    )
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name='项目名称')
    version = models.CharField(max_length=50, verbose_name='版本')
    type = models.CharField(max_length=50, verbose_name='类型', choices=ProjectType)
    description = models.CharField(max_length=1024, blank=True, null=True, verbose_name='描述')
    status = models.BooleanField(default=True, verbose_name='状态')
    LastUpdateTime = models.DateTimeField(auto_now=True, verbose_name='最近修改时间')
    createTime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, max_length=1024, verbose_name='创建人')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '项目'
        verbose_name_plural = '项目'


class ProjectDynamic(models.Model):
    """
    项目动态
    """
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, related_name='dynamic_project', on_delete=models.CASCADE, verbose_name='所属项目')
    time = models.DateTimeField(max_length=128, verbose_name='操作时间')
    type = models.CharField(max_length=50, verbose_name='操作类型')
    operationObject = models.CharField(max_length=50, verbose_name='操作对象')
    user = models.ForeignKey(User, blank=True, null=True, related_name='userName',
                             on_delete=models.SET_NULL, verbose_name='操作人')
    description = models.CharField(max_length=1024, blank=True, null=True, verbose_name='描述')

    def __unicode__(self):
        return self.type

    class Meta:
        verbose_name = '项目动态'
        verbose_name_plural = '项目动态'


class ProjectMember(models.Model):
    """
    项目成员
    """
    CHOICES = (
        ('超级管理员', '超级管理员'),
        ('开发人员', '开发人员'),
        ('测试人员', '测试人员')
    )
    id = models.AutoField(primary_key=True)
    permissionType = models.CharField(max_length=50, verbose_name='权限角色', choices=CHOICES)
    project = models.ForeignKey(Project, related_name='member_project', on_delete=models.CASCADE, verbose_name='所属项目')
    user = models.ForeignKey(User, related_name='member_user', on_delete=models.CASCADE, verbose_name='用户')

    def __unicode__(self):
        return self.permissionType

    def __str__(self):
        return self.permissionType

    class Meta:
        verbose_name = '项目成员'
        verbose_name_plural = '项目成员'


class GlobalHost(models.Model):
    """
    host域名
    """
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='项目')
    name = models.CharField(max_length=50, verbose_name='名称')
    host = models.CharField(max_length=1024, verbose_name='Host地址')
    description = models.CharField(max_length=1024, blank=True, null=True, verbose_name='描述')
    status = models.BooleanField(default=True, verbose_name='状态')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'HOST'
        verbose_name_plural = 'HOST管理'


"""高靖宇添加开始"""


class Sys_Project(models.Model):
    """
    系统
    项目表
    """

    id = models.AutoField(primary_key=True)
    project_name = models.CharField(max_length=100, verbose_name='项目名称')
    content = models.CharField(max_length=255, blank=True, null=True, verbose_name='描述')
    status = models.CharField(max_length=5, verbose_name='状态')

    LastUpdateTime = models.DateTimeField(auto_now=True, verbose_name='最近修改时间')
    createTime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    # 需要新建外键关联的主表才能设置外键
    # Project_id = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, max_length=1024, verbose_name='项目id')

    def __unicode__(self):
        return self.project_name

    def __str__(self):
        return self.project_name

    class Meta:
        db_table = 'sys_project'
        verbose_name = '项目名称'
        verbose_name_plural = '项目名称'


class Lyzd_Interface(models.Model):
    """
    龙盈智达
    接口信息表
    """

    id = models.AutoField(primary_key=True)
    interface_name_en = models.CharField(max_length=100, verbose_name='接口英文名称')

    interface_name_zh = models.CharField(max_length=100, verbose_name='接口中文名称')
    requestType = models.CharField(max_length=50, verbose_name='请求方式', choices=REQUEST_TYPE_CHOICE)
    authentication = models.CharField(max_length=100, verbose_name='认证')
    encryption = models.CharField(max_length=100, verbose_name='加密的接口url')
    decrypt = models.CharField(max_length=100, verbose_name='解密的接口url')
    delete_flag = models.CharField(max_length=5, verbose_name='删除标志')
    # requestParameterType
    create_user = models.CharField(max_length=100, verbose_name='创建用户')
    modify_user = models.CharField(max_length=100, verbose_name='修改用户')
    requestParameterType = models.CharField(max_length=50, verbose_name='修改用户')

    content = models.CharField(max_length=1024, blank=True, null=True, verbose_name='描述')
    LastUpdateTime = models.DateTimeField(auto_now=True, verbose_name='最近修改时间')
    createTime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    # 需要新建外键关联的主表才能设置外键
    Project_id = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, max_length=1024, verbose_name='项目id')

    def __unicode__(self):
        return self.interface_name_zh

    def __str__(self):
        return self.interface_name_zh

    class Meta:
        db_table = 'lyzd_interface'
        verbose_name = '接口信息'
        verbose_name_plural = '接口信息'


class Sys_Model(models.Model):
    """
    系统
    模块表
    """

    id = models.AutoField(primary_key=True)
    model_name = models.CharField(max_length=100, verbose_name='模块名称')

    # requestParameterType
    create_user = models.CharField(max_length=100, verbose_name='创建用户')
    modify_user = models.CharField(max_length=100, verbose_name='修改用户')
    status = models.CharField(max_length=5, verbose_name='状态')

    content = models.CharField(max_length=1024, blank=True, null=True, verbose_name='描述')

    testers = models.CharField(max_length=100, verbose_name='测试人员')
    developer = models.CharField(max_length=100, verbose_name='开发人员')

    LastUpdateTime = models.DateTimeField(auto_now=True, verbose_name='最近修改时间')
    createTime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    # 需要新建外键关联的主表才能设置外键
    Project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, max_length=1024, verbose_name='项目id')

    def __unicode__(self):
        return self.model_name

    def __str__(self):
        return self.model_name

    class Meta:
        db_table = 'sys_model'
        verbose_name = '模块表'
        verbose_name_plural = '模块信息'


class Sys_Environment(models.Model):
    """
    系统环境
    LyzdEnvironment
    高靖宇增加lyzdenvironment
    龙盈智达环境 测试
    """
    id = models.AutoField(primary_key=True)
    env_desc = models.CharField(max_length=100, verbose_name='环境名称')
    address = models.CharField(max_length=100, verbose_name='环境地址')
    content = models.CharField(max_length=255, verbose_name='描述')
    createTime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    LastUpdateTime = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __unicode__(self):
        return self.address

    def __str__(self):
        return self.address

    class Meta:
        db_table = 'sys_environment'
        verbose_name = '环境'
        verbose_name_plural = '环境管理'

# 接口入参表（interface_param）
class Lyzd_Interface_Param(models.Model):
    id = models.AutoField(primary_key=True)
    Interface_id = models.ForeignKey(Lyzd_Interface, on_delete=models.CASCADE, verbose_name="接口外键")
    param_key = models.CharField(max_length=50, verbose_name="入参key")
    param_type = models.CharField(max_length=50, verbose_name="入参类型",choices=PARAM_TYPE)
    random_number = models.CharField(max_length=50, verbose_name="随机数",choices=Random_Number)
    random_number_type = models.CharField(max_length=50, verbose_name="随机数_类型",choices=Random_Number_Type)
    createTime = models.DateTimeField(auto_now=True, verbose_name='创建时间')
    LastUpdateTime = models.DateTimeField(auto_now=True, verbose_name='最近修改时间')

    #     定义表名
    class Meta:
        db_table = 'lyzd_interface_param'
        verbose_name = '接口入参数表'
        verbose_name_plural = '接口入参数表'


# 接口header表（interface_header）：header是固定值
class Lyzd_Interface_Header(models.Model):
    id = models.AutoField(primary_key=True)
    interface_id = models.ForeignKey(Lyzd_Interface, on_delete=models.CASCADE, verbose_name="接口外键")
    header_key = models.CharField(max_length=50, verbose_name="headerKey")
    relation = models.CharField(max_length=5,  default= "0",verbose_name="依赖接口",choices=relation)
    relation_interface_id = models.CharField(max_length=50, verbose_name="依赖关系接口id")
    relation_interface_key = models.CharField(max_length=50, verbose_name="依赖关系headerKey")
    createTime = models.DateTimeField(auto_now=True, verbose_name='创建时间')
    LastUpdateTime = models.DateTimeField(auto_now=True, verbose_name='最近修改时间')

    #     定义表名
    class Meta:
        db_table = 'lyzd_interface_header'
        verbose_name = '接口header表'
        verbose_name_plural = '接口header表'

# 用例信息表（interface_case）
class Lyzd_Interface_Cases(models.Model):
    id = models.AutoField(primary_key=True)
    Interface_id = models.ForeignKey(Lyzd_Interface, on_delete=models.CASCADE,verbose_name="接口外键")
    case_name = models.CharField(max_length=50, verbose_name="用例名称")
    case_type = models.CharField(max_length=100, default= "2",verbose_name="用例分类",choices=Case_Type_CHOICE)
    check_type = models.CharField(max_length=100, default= "0",verbose_name="校验分类",choices=Check_Type_CHOICE)
    check_key = models.CharField(max_length=225, verbose_name="校验关键字") #去key值，如code,message
    check_condition = models.CharField(max_length=100, default='assertEqual',verbose_name="断言分类", choices=EXAMINE_TYPE_CHOICE) #属于断言分类
    check_value = models.CharField(max_length=225, verbose_name="预期值value")
    action_condition = models.CharField(max_length=225, default=0,verbose_name="执行条件",choices=Action_Condition_CHOICE)
    check_sql = models.CharField(max_length=225, verbose_name="执行sql")
    create_user = models.CharField(max_length=225, verbose_name="创建用户")
    modify_user = models.CharField(max_length=225, verbose_name="修改用户")
    status = models.BooleanField()
    def __str__(self):
        return str(self.id)
    #     定义表名
    class Meta:
        db_table = 'lyzd_interface_case'
        verbose_name = '用例信息表'
        verbose_name_plural = '用例信息表'



# 用例入参表（interface_case_param）：1个key存储1条记录
class Lyzd_Interface_Case_Param(models.Model):
    id = models.AutoField(primary_key=True)
    Interface_id = models.ForeignKey(Lyzd_Interface, on_delete=models.CASCADE, verbose_name="接口外键")
    Interface_Cases_id = models.ForeignKey(Lyzd_Interface_Cases, on_delete=models.CASCADE, verbose_name="测试用例外键")
    param_key = models.CharField(max_length=1024, verbose_name="入参key")
    param_value = models.CharField(max_length=1024, verbose_name="入参值value")
    create_user = models.CharField(max_length=225, verbose_name="创建用户")
    modify_user = models.CharField(max_length=225, verbose_name="修改用户")
    LastUpdateTime = models.DateTimeField(auto_now=True, verbose_name='最近修改时间')
    createTime = models.DateTimeField(auto_now=True, verbose_name='创建时间')



    #     定义表名  用例入参表
    class Meta:
        db_table = 'lyzd_interface_case_param'
        verbose_name = '用例入参表'
        verbose_name_plural = '用例入参表'



# 请求头入参表（interface_header_param）：
class Lyzd_Interface_Header_Param(models.Model):
    id = models.AutoField(primary_key=True)
    Interface_id = models.ForeignKey(Lyzd_Interface, on_delete=models.CASCADE, verbose_name="接口外键")
    Interface_Cases_id = models.ForeignKey(Lyzd_Interface_Cases, on_delete=models.CASCADE, verbose_name="测试用例外键")
    header_key = models.CharField(max_length=1024, verbose_name="请求头key")
    header_value = models.CharField(max_length=1024, verbose_name="请求头value")
    create_user = models.CharField(max_length=225, verbose_name="创建用户")
    modify_user = models.CharField(max_length=225, verbose_name="修改用户")
    LastUpdateTime = models.DateTimeField(auto_now=True, verbose_name='最近修改时间')
    createTime = models.DateTimeField(auto_now=True, verbose_name='创建时间')

    #     定义表名
    class Meta:
        db_table = 'lyzd_interface_header_param'



# 接口执行表（interface）:以接口得维度/类似于统计分析总表StatisticsData
class Lyzd_Interface_Action(models.Model):
    id = models.AutoField(primary_key=True)
    Project = models.ForeignKey(Sys_Project, on_delete=models.CASCADE, verbose_name="项目外键")
    environment_id = models.ForeignKey(Sys_Environment, on_delete=models.CASCADE, verbose_name="环境外键")
    # environment_id =  models.CharField(max_length=225,verbose_name="环境外键")
    interface_action = models.CharField(max_length=225, verbose_name="执行的接口")#总接口id
    interface_aciton_succcess = models.CharField(max_length=225, verbose_name="成功的接口")
    interface_aciton_fail = models.CharField(max_length=225, verbose_name="失败的接口")
    create_user = models.CharField(max_length=100, verbose_name="创建用户")
    LastUpdateTime = models.DateTimeField(auto_now=True, verbose_name='最近修改时间')
    createTime = models.DateTimeField(auto_now=True, verbose_name='创建时间')


    #     定义表名
    class Meta:
        db_table = 'lyzd_interface_action'


# 接口执行详情表（interface_action_detail） ：以用例得维度
class Lyzd_Interface_Action_Detail(models.Model):
    id = models.AutoField(primary_key=True)
    Interface_id = models.ForeignKey(Lyzd_Interface, on_delete=models.CASCADE, verbose_name="接口外键")
    Interface_Case_id = models.ForeignKey(Lyzd_Interface_Cases, on_delete=models.CASCADE, verbose_name="测试案例外键")
    param_in = models.CharField(max_length=1500, verbose_name="入参")  #总入参
    param_out = models.CharField(max_length=1500, verbose_name="出参")  #总出参
    check_key = models.CharField(max_length=225, verbose_name="校验关键字")  # 去key值，如code,message
    check_condition = models.CharField(max_length=100, verbose_name="断言分类")  # 属于断言分类
    check_value = models.CharField(max_length=225, verbose_name="预期值value")
    out_value = models.CharField(max_length=1225, verbose_name="实际返回值")
    action_condition = models.CharField(max_length=225, verbose_name="执行条件", default=0)  # 同时1条数据多个值校验得时候，多个结果是且/或得关系
    LastUpdateTime = models.DateTimeField(auto_now=True, verbose_name='最近修改时间')
    createTime = models.DateTimeField(auto_now=True, verbose_name='创建时间')


    #     定义表名
    class Meta:
        db_table = 'lyzd_interface_action_detail'



#任务表
class Lyzd_Task(models.Model):
    # Interfaces接口外键
    interface_name=models.ForeignKey(Lyzd_Interface,on_delete=models.CASCADE, verbose_name="接口名")
    task_name = models.CharField(max_length=200,verbose_name="任务名") #唯一
    uuid = models.CharField(max_length=200, default="")
    out_id = models.CharField(max_length=200, default="")
    carryId = models.IntegerField(default=0)
    task_run_time_regular = models.CharField(max_length=100,verbose_name="定时")
    ip=models.CharField(max_length=40,default="",verbose_name="Environments的ip")
    Nosqldb = models.CharField(max_length=40,default="")
    db = models.CharField(max_length=40,default="")
    email = models.CharField(max_length=40,default="",verbose_name="eaail的id")
    failcount = models.CharField(max_length=40,default="",verbose_name="执行失败次数")
    remark = models.CharField(max_length=200,verbose_name="任务备注")
    Nosqldb_desc = models.CharField(max_length=400,default="")
    db_remark = models.CharField(max_length=100, default="",verbose_name="db的备注")
    env_desc = models.CharField(max_length=100, default="",verbose_name="Environments的备注")
    subject = models.CharField(max_length=100, default="",verbose_name="email的标题名")
    status = models.BooleanField()
    carrystatus = models.IntegerField(default=2)
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now=True)

    #     定义表名
    class Meta:
        db_table = 'lyzd_task'


    def __str__(self):
        return str(self.task_name)



#第几次执行任务
class Lyzd_CarryTask(models.Model):
    task_name = models.CharField(max_length=200,verbose_name="任务名")
    htmlreport = models.CharField(max_length=200, default="")
    successlogname = models.CharField(max_length=200, default="")
    errorlogname = models.CharField(max_length=200, default="")
    stepcountall = models.IntegerField(default=0)
    stepcountnow = models.IntegerField(default=0)
    out_id = models.CharField(max_length=200, default="")
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now=True)


    #     定义表名
    class Meta:
        db_table = 'lyzd_carrytask'

    def __str__(self):
        return str(self.task_name)

#邮件配置表
class Lyzd_Email(models.Model):
    sender=models.CharField(max_length=100,verbose_name="发送人")
    receivers = models.CharField(max_length=100,verbose_name="接收人列表")
    host_dir = models.CharField(max_length=100,verbose_name="邮件主机")
    email_port=models.CharField(max_length=20, default="",verbose_name="邮件发送端口")
    username = models.CharField(max_length=100,verbose_name="用户名")
    passwd = models.CharField(max_length=100,verbose_name="密码")
    Headerfrom = models.CharField(max_length=100,verbose_name="发送人头部信息")
    Headerto = models.CharField(max_length=100,verbose_name="接收人头部信息")
    subject = models.CharField(max_length=100,default="",verbose_name="邮件标题",unique=True) #唯一

    def __str__(self):
        return str(self.username)

    #     定义表名
    class Meta:
        db_table = 'lyzd_email'

#邮件和日志的反馈
class Lyzd_LogAndHtmlfeedback(models.Model):
    test_step = models.CharField(max_length=100,verbose_name="步骤名")
    test_status = models.IntegerField(verbose_name="测试结果") #1表示成功 0表示接口内部错误500 2 表示断言错误
    test_response = models.CharField(max_length=225,verbose_name="测试返回值的message信息")
    test_carryTaskid = models.CharField(max_length=40,default="",verbose_name="第几次执行") #CarryTask的id
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.test_step)

        #     定义表名

    class Meta:
        db_table = 'lyzd_LogAndHtmlfeedback'



"""高靖宇添加结束"""


class CustomMethod(models.Model):
    """
    自定义方法
    """
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='项目')
    name = models.CharField(max_length=50, verbose_name='方法名')
    description = models.CharField(max_length=1024, blank=True, null=True, verbose_name='描述')
    type = models.CharField(max_length=50, verbose_name='类型')
    dataCode = models.TextField(verbose_name='代码')
    status = models.BooleanField(default=True, verbose_name='状态')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = '自定义方法'
        verbose_name_plural = '自定义方法'


class ApiGroupLevelFirst(models.Model):
    """
    接口一级分组
    """
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='项目')
    name = models.CharField(max_length=50, verbose_name='接口一级分组名称')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '接口分组'
        verbose_name_plural = '接口分组'


class ApiInfo(models.Model):
    """
    接口信息
    """
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, related_name='api_project', on_delete=models.CASCADE, verbose_name='所属项目')
    apiGroupLevelFirst = models.ForeignKey(ApiGroupLevelFirst, blank=True, null=True,
                                           related_name='First',
                                           on_delete=models.SET_NULL, verbose_name='所属一级分组')
    name = models.CharField(max_length=50, verbose_name='接口名称')
    httpType = models.CharField(max_length=50, default='HTTP', verbose_name='http/https', choices=HTTP_CHOICE)
    requestType = models.CharField(max_length=50, verbose_name='请求方式', choices=REQUEST_TYPE_CHOICE)
    apiAddress = models.CharField(max_length=1024, verbose_name='接口地址')
    requestParameterType = models.CharField(max_length=50, verbose_name='请求参数格式', choices=REQUEST_PARAMETER_TYPE_CHOICE)
    status = models.BooleanField(default=True, verbose_name='状态')
    mockStatus = models.BooleanField(default=False, verbose_name="mock状态")
    mockCode = models.CharField(max_length=50, blank=True, null=True, verbose_name='HTTP状态', choices=HTTP_CODE_CHOICE)
    data = models.TextField(blank=True, null=True, verbose_name='mock内容')
    lastUpdateTime = models.DateTimeField(auto_now=True, verbose_name='最近更新')
    userUpdate = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, max_length=50, verbose_name='更新人',
                                   related_name='ApiUpdateUser')
    description = models.CharField(max_length=1024, blank=True, null=True, verbose_name='描述')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '接口'
        verbose_name_plural = '接口管理'


class ApiHead(models.Model):
    id = models.AutoField(primary_key=True)
    api = models.ForeignKey(ApiInfo, on_delete=models.CASCADE, verbose_name="所属接口", related_name='headers')
    name = models.CharField(max_length=1024, verbose_name="标签")
    value = models.CharField(max_length=1024, blank=True, null=True, verbose_name='内容')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '请求头'
        verbose_name_plural = '请求头管理'


class ApiParameter(models.Model):
    id = models.AutoField(primary_key=True)
    api = models.ForeignKey(ApiInfo, on_delete=models.CASCADE, verbose_name="所属接口", related_name='requestParameter')
    name = models.CharField(max_length=1024, verbose_name="参数名")
    _type = models.CharField(default="String", max_length=1024, verbose_name='参数类型',
                             choices=(('Int', 'Int'), ('String', 'String')))
    value = models.CharField(max_length=1024, blank=True, null=True, verbose_name='参数值')
    required = models.BooleanField(default=True, verbose_name="是否必填")
    restrict = models.CharField(max_length=1024, blank=True, null=True, verbose_name="输入限制")
    description = models.CharField(max_length=1024, blank=True, null=True, verbose_name="描述")

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '请求参数'
        verbose_name_plural = '请求参数管理'


class ApiParameterRaw(models.Model):
    id = models.AutoField(primary_key=True)
    api = models.OneToOneField(ApiInfo, on_delete=models.CASCADE, verbose_name="所属接口",
                               related_name='requestParameterRaw')
    data = models.TextField(blank=True, null=True, verbose_name='内容')

    class Meta:
        verbose_name = '请求参数Raw'


class ApiResponse(models.Model):
    id = models.AutoField(primary_key=True)
    api = models.ForeignKey(ApiInfo, on_delete=models.CASCADE, verbose_name="所属接口", related_name='response')
    name = models.CharField(max_length=1024, verbose_name="参数名")
    _type = models.CharField(default="String", max_length=1024, verbose_name='参数类型',
                             choices=(('Int', 'Int'), ('String', 'String')))
    value = models.CharField(max_length=1024, blank=True, null=True, verbose_name='参数值')
    required = models.BooleanField(default=True, verbose_name="是否必含")
    description = models.CharField(max_length=1024, blank=True, null=True, verbose_name="描述")

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '返回参数'
        verbose_name_plural = '返回参数管理'


class APIRequestHistory(models.Model):
    """
    接口请求历史
    """
    id = models.AutoField(primary_key=True)
    api = models.ForeignKey(ApiInfo, on_delete=models.CASCADE, verbose_name='接口')
    requestTime = models.DateTimeField(auto_now_add=True, verbose_name='请求时间')
    requestType = models.CharField(max_length=50, verbose_name='请求方法')
    requestAddress = models.CharField(max_length=1024, verbose_name='请求地址')
    httpCode = models.CharField(max_length=50, verbose_name='HTTP状态')

    def __unicode__(self):
        return self.requestAddress

    class Meta:
        verbose_name = '接口请求历史'
        verbose_name_plural = '接口请求历史'


class ApiOperationHistory(models.Model):
    """
    API操作历史
    """
    id = models.AutoField(primary_key=True)
    api = models.ForeignKey(ApiInfo, on_delete=models.CASCADE, verbose_name='接口')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, max_length=50, verbose_name='用户姓名')
    time = models.DateTimeField(auto_now_add=True, verbose_name='操作时间')
    description = models.CharField(max_length=1024, blank=True, null=True, verbose_name='操作内容')

    def __unicode__(self):
        return self.description

    class Meta:
        verbose_name = '接口操作历史'
        verbose_name_plural = '接口操作历史'


class AutomationGroupLevelFirst(models.Model):
    """
    自动化用例一级分组
    """
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='项目')
    name = models.CharField(max_length=50, verbose_name='用例一级分组')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '用例分组'
        verbose_name_plural = '用例分组管理'


class AutomationTestCase(models.Model):
    """
    自动化测试用例
    """
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='所属项目')
    automationGroupLevelFirst = models.ForeignKey(AutomationGroupLevelFirst, blank=True, null=True,
                                                  on_delete=models.SET_NULL, verbose_name='所属用例一级分组',
                                                  related_name="automationGroup")
    # automationGroupLevelSecond = models.ForeignKey(AutomationGroupLevelSecond, blank=True, null=True,
    #                                                on_delete=models.SET_NULL, verbose_name='所属用例二级分组')
    caseName = models.CharField(max_length=50, verbose_name='用例名称')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="创建人",
                             related_name="createUser")
    description = models.CharField(max_length=1024, blank=True, null=True, verbose_name='描述')
    updateTime = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __unicode__(self):
        return self.caseName

    def __str__(self):
        return self.caseName

    class Meta:
        verbose_name = '自动化测试用例'
        verbose_name_plural = '自动化测试用例'


class AutomationCaseApi(models.Model):
    """
    用例执行接口
    """
    id = models.AutoField(primary_key=True)
    automationTestCase = models.ForeignKey(AutomationTestCase, on_delete=models.CASCADE,
                                           verbose_name='用例', related_name="api")
    name = models.CharField(max_length=50, verbose_name='接口名称')
    httpType = models.CharField(max_length=50, default='HTTP', verbose_name='HTTP/HTTPS', choices=HTTP_CHOICE)
    requestType = models.CharField(max_length=50, verbose_name='请求方式', choices=REQUEST_TYPE_CHOICE)
    apiAddress = models.CharField(max_length=1024, verbose_name='接口地址')
    requestParameterType = models.CharField(max_length=50, verbose_name='参数请求格式', choices=REQUEST_PARAMETER_TYPE_CHOICE)
    formatRaw = models.BooleanField(default=False, verbose_name="是否转换成源数据")
    examineType = models.CharField(default='no_check', max_length=50, verbose_name='校验方式', choices=EXAMINE_TYPE_CHOICE)
    httpCode = models.CharField(max_length=50, blank=True, null=True, verbose_name='HTTP状态', choices=HTTP_CODE_CHOICE)
    responseData = models.TextField(blank=True, null=True, verbose_name='返回内容')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '用例接口'
        verbose_name_plural = '用例接口管理'


class AutomationHead(models.Model):
    """
    请求头
    """
    id = models.AutoField(primary_key=True)
    automationCaseApi = models.ForeignKey(AutomationCaseApi, related_name='header',
                                          on_delete=models.CASCADE, verbose_name='接口')
    name = models.CharField(max_length=1024, verbose_name='参数名')
    value = models.CharField(max_length=1024, verbose_name='内容')
    interrelate = models.BooleanField(default=False, verbose_name='是否关联')

    def __unicode__(self):
        return self.value

    class Meta:
        verbose_name = '请求头'
        verbose_name_plural = '请求头管理'


class AutomationParameter(models.Model):
    """
    请求的参数
    """
    id = models.AutoField(primary_key=True)
    automationCaseApi = models.ForeignKey(AutomationCaseApi, related_name='parameterList',
                                          on_delete=models.CASCADE, verbose_name='接口')
    name = models.CharField(max_length=1024, verbose_name='参数名')
    value = models.CharField(max_length=1024, verbose_name='内容', blank=True, null=True)
    interrelate = models.BooleanField(default=False, verbose_name='是否关联')

    def __unicode__(self):
        return self.value

    class Meta:
        verbose_name = '接口参数'
        verbose_name_plural = '接口参数管理'


class AutomationParameterRaw(models.Model):
    """
    请求的源数据参数
    """
    id = models.AutoField(primary_key=True)
    automationCaseApi = models.OneToOneField(AutomationCaseApi, related_name='parameterRaw',
                                             on_delete=models.CASCADE, verbose_name='接口')
    data = models.TextField(verbose_name='源数据请求参数', blank=True, null=True)

    class Meta:
        verbose_name = '源数据参数'
        verbose_name_plural = '源数据参数管理'


class AutomationResponseJson(models.Model):
    """
    返回JSON参数
    """
    id = models.AutoField(primary_key=True)
    automationCaseApi = models.ForeignKey(AutomationCaseApi, related_name='response',
                                          on_delete=models.CASCADE, verbose_name='接口')
    name = models.CharField(max_length=1024, verbose_name='JSON参数', blank=True, null=True)
    tier = models.CharField(max_length=1024, verbose_name='层级关系', blank=True, null=True)
    type = models.CharField(max_length=1024, verbose_name="关联类型", default="json",
                            choices=(('json', 'json'), ('Regular', 'Regular')))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '结果JSON参数'
        verbose_name_plural = '结果JSON参数管理'


class AutomationTestResult(models.Model):
    """
    手动执行结果
    """
    id = models.AutoField(primary_key=True)
    automationCaseApi = models.OneToOneField(AutomationCaseApi, on_delete=models.CASCADE, verbose_name='接口'
                                             , related_name="test_result")
    url = models.CharField(max_length=1024, verbose_name='请求地址')
    requestType = models.CharField(max_length=1024, verbose_name='请求方式', choices=REQUEST_TYPE_CHOICE)
    host = models.CharField(max_length=1024, verbose_name='测试地址', null=True, blank=True)
    header = models.CharField(max_length=1024, blank=True, null=True, verbose_name='请求头')
    parameter = models.TextField(blank=True, null=True, verbose_name='请求参数')
    statusCode = models.CharField(blank=True, null=True, max_length=1024, verbose_name='期望HTTP状态',
                                  choices=HTTP_CODE_CHOICE)
    examineType = models.CharField(max_length=1024, verbose_name='匹配规则')
    data = models.TextField(blank=True, null=True, verbose_name='规则内容')
    result = models.CharField(max_length=50, verbose_name='测试结果', choices=RESULT_CHOICE)
    httpStatus = models.CharField(max_length=50, blank=True, null=True, verbose_name='http状态', choices=HTTP_CODE_CHOICE)
    responseData = models.TextField(blank=True, null=True, verbose_name='实际返回内容')
    testTime = models.DateTimeField(auto_now_add=True, verbose_name='测试时间')

    def __unicode__(self):
        return self.httpStatus

    class Meta:
        verbose_name = '手动测试结果'
        verbose_name_plural = '手动测试结果管理'


class AutomationTestTask(models.Model):
    """
    用例定时任务
    """
    id = models.AutoField(primary_key=True)
    project = models.OneToOneField(Project, on_delete=models.CASCADE, verbose_name='项目')
    Host = models.ForeignKey(GlobalHost, on_delete=models.CASCADE, verbose_name='HOST')
    name = models.CharField(max_length=50, verbose_name='任务名称')
    type = models.CharField(max_length=50, verbose_name='类型', choices=TASK_CHOICE)
    frequency = models.IntegerField(blank=True, null=True, verbose_name='间隔')
    unit = models.CharField(max_length=50, blank=True, null=True, verbose_name='单位', choices=UNIT_CHOICE)
    startTime = models.DateTimeField(max_length=50, verbose_name='开始时间')
    endTime = models.DateTimeField(max_length=50, verbose_name='结束时间')

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '用例定时任务'
        verbose_name_plural = '用例定时任务管理'


class AutomationTaskRunTime(models.Model):
    """
    用例执行开始和结束时间
    """
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='项目')
    startTime = models.CharField(max_length=50, verbose_name='开始时间')
    host = models.CharField(max_length=1024, null=True, blank=True, verbose_name='测试地址')
    elapsedTime = models.CharField(max_length=50, verbose_name='结束时间')

    class Meta:
        verbose_name = '用例任务执行时间'
        verbose_name_plural = '用例任务执行时间'


class AutomationCaseTestResult(models.Model):
    """
    任务执行结果
    """
    id = models.AutoField(primary_key=True)
    automationCaseApi = models.ForeignKey(AutomationCaseApi, on_delete=models.CASCADE, verbose_name='接口'
                                          , related_name="auto_result")
    header = models.CharField(max_length=1024, blank=True, null=True, verbose_name='请求头')
    parameter = models.TextField(blank=True, null=True, verbose_name='请求参数')
    result = models.CharField(max_length=50, verbose_name='测试结果', choices=RESULT_CHOICE)
    httpStatus = models.CharField(max_length=50, blank=True, null=True, verbose_name='http状态', choices=HTTP_CODE_CHOICE)
    responseHeader = models.TextField(blank=True, null=True, verbose_name='返回头')
    responseData = models.TextField(blank=True, null=True, verbose_name='实际返回内容')
    testTime = models.CharField(max_length=128, null=True, blank=True, verbose_name='测试时间')

    def __unicode__(self):
        return self.httpStatus

    class Meta:
        verbose_name = '自动测试结果'
        verbose_name_plural = '自动测试结果管理'


class AutomationReportSendConfig(models.Model):
    """
    报告发送人配置
    """
    id = models.AutoField(primary_key=True)
    project = models.OneToOneField(Project, on_delete=models.CASCADE, verbose_name="项目")
    reportFrom = models.EmailField(max_length=1024, blank=True, null=True, verbose_name="发送人邮箱")
    mailUser = models.CharField(max_length=1024, blank=True, null=True, verbose_name="用户名")
    mailPass = models.CharField(max_length=1024, blank=True, null=True, verbose_name="口令")
    mailSmtp = models.CharField(max_length=1024, blank=True, null=True, verbose_name="邮箱服务器")

    def __unicode__(self):
        return self.reportFrom

    class Meta:
        verbose_name = "邮件发送配置"
        verbose_name_plural = "邮件发送配置"


class VisitorsRecord(models.Model):
    """
    访客记录
    """
    id = models.AutoField(primary_key=True)
    formattedAddress = models.CharField(max_length=1024, blank=True, null=True, verbose_name="访客地址")
    country = models.CharField(max_length=50, blank=True, null=True, verbose_name="国家")
    province = models.CharField(max_length=50, blank=True, null=True, verbose_name="省份")
    city = models.CharField(max_length=50, blank=True, null=True, verbose_name="城市")
    district = models.CharField(max_length=50, blank=True, null=True, verbose_name="县级")
    township = models.CharField(max_length=50, blank=True, null=True, verbose_name="镇")
    street = models.CharField(max_length=50, blank=True, null=True, verbose_name="街道")
    number = models.CharField(max_length=50, blank=True, null=True, verbose_name="门牌号")
    success = models.CharField(max_length=50, blank=True, null=True, verbose_name="成功")
    reason = models.CharField(max_length=1024, blank=True, null=True, verbose_name="原因")
    callTime = models.DateTimeField(auto_now_add=True, verbose_name="访问时间")

    def __unicode__(self):
        return self.formattedAddress

    class Meta:
        verbose_name = "访客"
        verbose_name_plural = "访客查看"
