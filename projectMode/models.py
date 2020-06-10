from django.db import models

# Create your models here.

# 自定义项目所属模块
Module_Choice = (
    ('caseList', '接口测试'),
    ('webTest', 'web测试'),
    ('appTest', 'app测试'),
    ('bugManage', 'BUG管理'),
    ('report', '测试报告'),
    ('testTool', '常用测试工具')
)
# 子类枚举
Sub_Type = (
    ('testCase', '空'),
    ('order', '订单处理'),
    ('download', '下载')
)
# 数据库类型枚举
DB_Type_Choice = (
    (1, "MySql"),
    (2, "SqlServer"),
    (3, "Oracle"),
    (4, "MongoDB")
)


# 项目信息表
class ProjectMode(models.Model):
    projectName = models.CharField('项目名称', max_length=50)
    projectFlag = models.BooleanField('项目状态', default=True)
    projectTag = models.CharField('项目标识', max_length=50, unique=True)
    createName = models.CharField('创建人', max_length=50)
    createTime = models.DateTimeField('创建时间', auto_now_add=True)
    module = models.CharField(
        '项目所属模块', choices=Module_Choice, max_length=50)
    productId = models.ForeignKey(
        'projectMode.ProductMode', on_delete=models.CASCADE)
    subType = models.CharField(
        '子类', max_length=50, choices=Sub_Type, default='')

    class Meta:
        verbose_name = '项目信息'
        verbose_name_plural = '项目信息'

    def __str__(self):
        return self.projectName


# 产品关系表
class ProductMode(models.Model):
    productName = models.CharField('产品名称', max_length=50)
    productFlag = models.BooleanField('产品状态', default=True)
    productTag = models.CharField('产品标识', max_length=50)
    createName = models.CharField('创建人', max_length=50)
    createTime = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '产品信息'
        verbose_name_plural = '产品信息'

    def __str__(self):
        return self.productName


# 数据库配置表
class DBConfigMode(models.Model):
    dbName = models.CharField('配置名称', max_length=50)
    dbType = models.IntegerField('数据库类型', choices=DB_Type_Choice)
    dbServer = models.CharField('服务器ip&端口', max_length=50)
    dbAccount = models.CharField('账号', max_length=50)
    dbPassWord = models.CharField('密码', max_length=50)
    dbDefault = models.CharField('默认数据库', max_length=50)
    dbFlag = models.BooleanField('配置有效性', default=True)

    class Meta:
        verbose_name = '数据库配置'
        verbose_name_plural = '数据库配置'

    def __str__(self):
        return self.dbName
