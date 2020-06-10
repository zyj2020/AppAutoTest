# Generated by Django 2.2.5 on 2020-05-28 04:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projectMode', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApiMode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('apiName', models.CharField(max_length=50, verbose_name='接口名')),
                ('apiDesc', models.CharField(max_length=200, verbose_name='接口描述')),
                ('apiFlg', models.BooleanField(default=True, verbose_name='接口有效性')),
                ('apiUrl', models.URLField(verbose_name='接口地址')),
                ('apiRequestType', models.CharField(choices=[('POST', 'POST'), ('GET', 'GET')], max_length=50, verbose_name='接口请求方式')),
                ('apiHeader', models.CharField(choices=[('application/json', 'application/json'), ('text/json', 'text/json'), ('application/xml', 'application/xml'), ('text/xml', 'text/xml'), ('application/x-www-form-urlencoded', 'application/x-www-form-urlencoded'), ('', '无')], max_length=50, verbose_name='接口请求头')),
                ('apiHeaderEsp', models.TextField(blank=True, default=True, verbose_name='特殊请求头')),
                ('apiDefaultRequest', models.TextField(blank=True, default=True, verbose_name='接口默认请求参数')),
            ],
            options={
                'verbose_name': 'API表',
                'verbose_name_plural': 'API表',
            },
        ),
        migrations.CreateModel(
            name='TaskRunLogMode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('taskId', models.IntegerField(verbose_name='测试计划ID')),
                ('taskOperator', models.CharField(max_length=50, verbose_name='任务执行人')),
                ('runTime', models.DateTimeField(auto_now_add=True, verbose_name='执行时间')),
                ('runCaseNum', models.IntegerField(verbose_name='执行用例数')),
                ('passNum', models.IntegerField(verbose_name='通过数量')),
                ('failNum', models.IntegerField(verbose_name='失败数量')),
                ('result', models.TextField(verbose_name='执行结果')),
                ('failLogList', models.TextField(verbose_name='失败用例日志集合')),
            ],
            options={
                'verbose_name': '任务执行日志',
                'verbose_name_plural': '任务执行日志',
                'ordering': ('-runTime',),
            },
        ),
        migrations.CreateModel(
            name='TestCaseMode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caseName', models.CharField(max_length=50, verbose_name='用例名称')),
                ('caseDes', models.CharField(max_length=200, verbose_name='用例描述')),
                ('caseFlg', models.BooleanField(default=True, verbose_name='用例状态')),
                ('productId', models.IntegerField(verbose_name='产品ID')),
                ('caseLevel', models.IntegerField(choices=[(1, '核心用例'), (2, '一般用例'), (3, '次要用例')], verbose_name='用例等级')),
                ('caseEnv', models.IntegerField(choices=[(1, '开发环境'), (2, '预发环境'), (3, '正式环境')], verbose_name='执行环境')),
                ('projectId', models.IntegerField(verbose_name='项目ID')),
                ('groupApiId', models.IntegerField(verbose_name='接口组ID')),
                ('caseBody', models.TextField(verbose_name='请求参数')),
                ('excRule', models.TextField(verbose_name='匹配规则')),
                ('actResult', models.TextField(verbose_name='实际结果')),
                ('actNum', models.IntegerField(default=0, verbose_name='执行次数')),
                ('createName', models.CharField(max_length=20, verbose_name='创建人')),
                ('createTime', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('apiId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apiTest.ApiMode')),
            ],
            options={
                'verbose_name': '用例详情',
                'verbose_name_plural': '用例详情',
            },
        ),
        migrations.CreateModel(
            name='TaskPlanMode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('taskPlanName', models.CharField(max_length=50, verbose_name='测试计划名')),
                ('taskPlanCaseApiList', models.CharField(max_length=2000, verbose_name='执行接口集合')),
                ('taskPlanCaseLevel', models.CharField(max_length=200, verbose_name='执行用例等级')),
                ('taskPlanRun', models.IntegerField(choices=[(1, '开发环境'), (2, '预发环境'), (3, '正式环境')], null=True, verbose_name='计划执行环境')),
                ('taskPlanFlg', models.BooleanField(default=True, verbose_name='计划有效性')),
                ('taskPlanIteration', models.IntegerField(default=0, verbose_name='迭代次数')),
                ('createName', models.CharField(max_length=50, verbose_name='创建人')),
                ('createTime', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('projectId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projectMode.ProjectMode')),
            ],
            options={
                'verbose_name': '测试计划',
                'verbose_name_plural': '测试计划',
            },
        ),
        migrations.CreateModel(
            name='GroupApiMode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('groupName', models.CharField(max_length=50, verbose_name='组名')),
                ('groupDesc', models.CharField(max_length=200, verbose_name='描述')),
                ('groupFlg', models.BooleanField(default=True, verbose_name='属性')),
                ('projectId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projectMode.ProjectMode')),
            ],
            options={
                'verbose_name': '接口组',
                'verbose_name_plural': '接口组',
            },
        ),
        migrations.CreateModel(
            name='EnvConfigMode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('testUrl', models.URLField(verbose_name='开发环境')),
                ('releseUrl', models.URLField(verbose_name='预发环境')),
                ('productUrl', models.URLField(verbose_name='正式环境')),
                ('projectId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projectMode.ProjectMode')),
            ],
            options={
                'verbose_name': '环境配置',
                'verbose_name_plural': '环境配置',
            },
        ),
        migrations.CreateModel(
            name='CaseRunLogMode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('apiId', models.IntegerField(verbose_name='接口ID')),
                ('runTime', models.DateTimeField(auto_now_add=True, verbose_name='测试时间')),
                ('runResult', models.CharField(max_length=50, verbose_name='测试结果')),
                ('actResult', models.TextField(verbose_name='实际结果')),
                ('caseBody', models.TextField(verbose_name='请求参数')),
                ('projectId', models.IntegerField(verbose_name='项目ID')),
                ('logType', models.IntegerField(verbose_name='日志类型')),
                ('caseId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apiTest.TestCaseMode')),
            ],
            options={
                'verbose_name': '用例执行日志',
                'verbose_name_plural': '用例执行日志',
                'ordering': ('-runTime',),
            },
        ),
        migrations.CreateModel(
            name='ApiSqlListMode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('apiSqlName', models.CharField(max_length=50, unique=True, verbose_name='sql名称')),
                ('apiSqlNameInfo', models.TextField(verbose_name='sql语句')),
                ('projectId', models.IntegerField(verbose_name='项目ID')),
                ('apiSqlFlg', models.BooleanField(default=True, verbose_name='有效性')),
                ('createName', models.CharField(max_length=50, verbose_name='创建人')),
                ('createTime', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('apiId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apiTest.ApiMode')),
                ('dbconfId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projectMode.DBConfigMode')),
            ],
            options={
                'verbose_name': '接口自定义SQL',
                'verbose_name_plural': '接口自定义SQL',
            },
        ),
        migrations.AddField(
            model_name='apimode',
            name='groupApiId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apiTest.GroupApiMode'),
        ),
        migrations.CreateModel(
            name='UserVarMode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('varType', models.IntegerField(verbose_name='变量类型')),
                ('varName', models.CharField(max_length=200, verbose_name='变量名')),
                ('varValue', models.TextField(verbose_name='变量值')),
                ('varDesc', models.TextField(verbose_name='变量描述')),
                ('projectId', models.IntegerField(verbose_name='项目ID')),
                ('varFlg', models.BooleanField(default=True, verbose_name='有效性')),
                ('sceneId', models.IntegerField(verbose_name='场景ID')),
                ('apiId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='apiTest.ApiMode')),
            ],
            options={
                'verbose_name': '自定义变量',
                'verbose_name_plural': '自定义变量',
                'unique_together': {('varName', 'apiId', 'projectId')},
            },
        ),
    ]
