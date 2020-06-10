# Generated by Django 2.2.5 on 2020-06-04 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projectMode', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='projectmode',
            old_name='CharField',
            new_name='projectTag',
        ),
        migrations.AlterField(
            model_name='projectmode',
            name='module',
            field=models.CharField(choices=[('caseList', '接口测试'), ('webTest', 'web测试'), ('appTest', 'app测试'), ('bugManage', 'BUG管理'), ('report', '测试报告'), ('testTool', '常用测试工具')], max_length=50, verbose_name='项目所属模块'),
        ),
    ]