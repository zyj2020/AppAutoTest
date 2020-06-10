# import __init__
from django.contrib import admin
from apiTest.models import TestCaseMode, GroupApiMode, ApiMode, \
    EnvConfigMode, TaskPlanMode, CaseRunLogMode, \
    UserVarMode, ApiSqlListMode, TaskRunLogMode
from projectMode.models import ProjectMode

# Register your models here.


# 要开始注册了， 开始注册测试用例
class TestCaseAdmin(admin.ModelAdmin):
    # 呈现项目列表
    list_display = ['id', 'caseName', 'caseLevel', 'caseEnv', 'caseBody', 'excRule', 'actResult', 'actNum']


# 自定义变量
class UserVarAdmin(admin.ModelAdmin):
    exclude = ('varType', 'apiId', 'scenarioId',)  # 隐藏这些字段

    def save_model(self, request, obj, form, change):
        try:
            api = None
            project_id = request.GET.get('projectId')
            api_id = request.GET.get('apiId')
            var_type = request.GET.get('varType')
            s_id = request.GET.get('sId')
            if int(api_id) > 0:
                api = ApiMode.objects.get(id=api_id)
            obj.projectId = project_id
            obj.varType = var_type
            obj.apiId = api
            obj.sceneId = s_id
        except(ValueError, TypeError):
            pass
        super(UserVarAdmin, self).save_model(request, obj, form, change)


# 接口自定义
class ApiSqlListAdmin(admin.ModelAdmin):
    exclude = ('apiId', 'projectId')  # 隐藏

    def save_model(self, request, obj, form, change):
        try:
            project_id = request.GET.get('projectId')
            api_id = request.GET.get('apiId')
            api = ApiMode.objects.get(id=api_id)
            obj.projectId = project_id
            obj.apiId = api
        except(ValueError, TypeError):
            pass
        super(ApiSqlListAdmin, self).save_model(request, obj, form, change)


# Api组定义
class GroupApiAdmin(admin.ModelAdmin):
    # exclude = ('projectId',)  # 隐藏

    def save_model(self, request, obj, form, change):
        try:
            project_id = request.GET.get('projectId')
            pro = ProjectMode.objects.get(id=project_id)
            obj.projectId = pro
        except(ValueError, TypeError):
            pass
        super(GroupApiAdmin, self).save_model(request, obj, form, change)


admin.site.register(TestCaseMode)
admin.site.register(GroupApiMode, GroupApiAdmin)
admin.site.register(ApiMode)
admin.site.register(EnvConfigMode)
admin.site.register(TaskPlanMode)
admin.site.register(CaseRunLogMode)
admin.site.register(ApiSqlListMode, ApiSqlListAdmin)
admin.site.register(UserVarMode, UserVarAdmin)
admin.site.register(TaskRunLogMode)
