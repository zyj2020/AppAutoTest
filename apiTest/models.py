from django.db import models
from projectMode.models import ProjectMode, ProductMode, DBConfigMode

# Create your models here.
# 自定义变量
# 用例等级
Case_Level_Choice = (
    (1, "核心用例"),
    (2, "一般用例"),
    (3, "次要用例")
)
# 执行环境
Case_Env_Choice = (
    (1, "开发环境"),
    (2, "预发环境"),
    (3, "正式环境")
)


# 测试用例表信息
class TestCaseMode(models.Model):
    caseName = models.CharField('用例名称', max_length=50)
    caseDes = models.CharField('用例描述', max_length=200)
    caseFlg = models.BooleanField('用例状态', default=True)
    productId = models.IntegerField('产品ID')
    caseLevel = models.IntegerField('用例等级', choices=Case_Level_Choice)
    caseEnv = models.IntegerField('执行环境', choices=Case_Env_Choice)
    projectId = models.IntegerField('项目ID')
    groupApiId = models.IntegerField('接口组ID')
    apiId = models.ForeignKey('ApiMode', on_delete=models.CASCADE, null=False)
    caseBody = models.TextField('请求参数')
    excRule = models.TextField('匹配规则')
    actResult = models.TextField('实际结果')
    actNum = models.IntegerField('执行次数', default=0)
    creator = models.CharField('创建人', max_length=20)
    createTime = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '用例详情'
        verbose_name_plural = '用例详情'

    def __str__(self):
        return self.caseName


# API组表
class GroupApiMode(models.Model):
    groupName = models.CharField('组名', max_length=50)
    groupDesc = models.CharField('描述', max_length=200)
    groupFlg = models.BooleanField('有效属性', default=True)
    projectId = models.ForeignKey(
        'projectMode.ProjectMode', on_delete=models.CASCADE, null=False)

    class Meta:
        verbose_name = '接口组'
        verbose_name_plural = '接口组'

    def __str__(self):
        return self.groupName


# 请求类型
Type_Choice = (
    ('POST', 'POST'),
    ('GET', 'GET')
)
# 请求头
Header_Choice = (
    ('application/json', 'application/json'),
    ('text/json', 'text/json'),
    ('application/xml', 'application/xml'),
    ('text/xml', 'text/xml'),
    ('application/x-www-form-urlencoded', 'application/x-www-form-urlencoded'),
    ('', '无')
)


# API表
class ApiMode(models.Model):
    apiName = models.CharField('接口名', max_length=50)
    apiDesc = models.CharField('接口描述', max_length=200)
    apiFlg = models.BooleanField('接口有效性', default=True)
    groupApiId = models.ForeignKey(
        'apiTest.GroupApiMode', on_delete=models.CASCADE, null=False)
    apiUrl = models.URLField('接口地址', max_length=200)
    apiRequestType = models.CharField(
        '接口请求方式', max_length=50, choices=Type_Choice)
    apiHeader = models.CharField(
        '接口请求头', max_length=50, choices=Header_Choice)
    apiHeaderEsp = models.TextField('特殊请求头', default=True, blank=True)
    apiDefaultRequest = models.TextField('接口默认请求参数', default=True, blank=True)

    class Meta:
        verbose_name = 'API表'
        verbose_name_plural = 'API表'

    def __str__(self):
        return self.apiName


# 环境配置表
class EnvConfigMode(models.Model):
    projectId = models.ForeignKey('projectMode.ProjectMode', on_delete=models.CASCADE, null=False)
    localUrl = models.URLField("本地地址", default='')
    testUrl = models.URLField("测试地址")
    releaseUrl = models.URLField("预发地址")
    productUrl = models.URLField("正式地址")

    class Meta:
        verbose_name = '执行环境配置'
        verbose_name_plural = '执行环境配置'


# 测试计划表
class TaskPlanMode(models.Model):
    taskPlanName = models.CharField('测试计划名', max_length=50)
    taskPlanCaseApiList = models.CharField('执行接口集合', max_length=2000)
    taskPlanCaseLevel = models.CharField('执行用例等级', max_length=200)
    taskPlanRun = models.IntegerField(
        '计划执行环境', choices=Case_Env_Choice, null=True)
    taskPlanFlg = models.BooleanField('计划有效性', default=True)
    taskPlanIteration = models.IntegerField('迭代次数', default=0)
    creator = models.CharField('创建人', max_length=50)
    createTime = models.DateTimeField('创建时间', auto_now_add=True)
    projectId = models.ForeignKey(
        'projectMode.ProjectMode', on_delete=models.CASCADE)

    class Meta:
        verbose_name = '测试计划'
        verbose_name_plural = '测试计划'

    def __str__(self):
        return self.taskPlanName


# 用例日志记录表
class CaseRunLogMode(models.Model):
    apiId = models.IntegerField('接口ID')
    caseId = models.ForeignKey(
        'apiTest.TestCaseMode', on_delete=models.CASCADE)
    runTime = models.DateTimeField('测试时间', auto_now_add=True)
    runResult = models.CharField('测试结果', max_length=50)
    actResult = models.TextField('实际结果')
    caseBody = models.TextField('请求参数')
    projectId = models.IntegerField('项目ID')
    logType = models.IntegerField('日志类型')

    class Meta:
        verbose_name = '用例执行日志'
        verbose_name_plural = '用例执行日志'
        ordering = ('-runTime',)


# 自定义变量表
class UserVarMode(models.Model):
    varType = models.IntegerField('变量类型', default=0)  # 0全局变量，1接口变量，2场景变量
    varName = models.CharField('变量名', max_length=200)
    varValue = models.TextField('变量值')
    varDesc = models.TextField('变量描述')
    projectId = models.IntegerField('项目ID')
    apiId = models.ForeignKey('apiTest.ApiMode', on_delete=models.CASCADE)
    varFlg = models.BooleanField('有效性', default=True)
    sceneId = models.IntegerField('场景ID')

    class Meta:
        unique_together = ('varName', 'apiId', 'projectId')
        verbose_name = '自定义变量'
        verbose_name_plural = '自定义变量'

    def __str__(self):
        return self.varName


# 接口自定义SQL表
class ApiSqlListMode(models.Model):
    apiSqlName = models.CharField('sql名称', max_length=50, unique=True)
    apiSqlNameInfo = models.TextField('sql语句')
    apiId = models.ForeignKey('apiTest.ApiMode', on_delete=models.CASCADE)
    dbconfId = models.ForeignKey(
        'projectMode.DBConfigMode', on_delete=models.CASCADE)
    projectId = models.IntegerField('项目ID')
    apiSqlFlg = models.BooleanField('有效性', default=True)
    creator = models.CharField('创建人', max_length=50)
    createTime = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '接口自定义SQL'
        verbose_name_plural = '接口自定义SQL'

    def __str__(self):
        return self.apiSqlName


# 任务执行日志
class TaskRunLogMode(models.Model):
    taskId = models.IntegerField('测试计划ID')
    creator = models.CharField('任务执行人', max_length=50)
    runTime = models.DateTimeField('执行时间', auto_now_add=True)
    runCaseNum = models.IntegerField('执行用例数')
    passNum = models.IntegerField('通过数量')
    failNum = models.IntegerField('失败数量')
    result = models.TextField('执行结果')
    failLogList = models.TextField('失败用例日志集合')

    class Meta:
        verbose_name = '任务执行日志'
        verbose_name_plural = '任务执行日志'
        ordering = ('-runTime',)
