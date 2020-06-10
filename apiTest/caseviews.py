from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required
from publicMode.views import get_list
from apiTest.models import GroupApiMode, ApiMode, EnvConfigMode, \
    TaskPlanMode, TestCaseMode, ApiSqlListMode, UserVarMode, CaseRunLogMode, \
    TaskRunLogMode
from projectMode.models import ProjectMode
from django.views.decorators.csrf import csrf_exempt
import json
from apiTest.server import run_cases, run, run_base_case, run_task
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
import copy


# Create your views here.


@login_required
def case_entry(request):
    """测试用例初始页面"""
    res = get_list("caseList")
    return render(request, "caseList_manage.html", {"products": res[0], "projects": res[1]})


@login_required
def case_list(request, project):
    """测试用例列表页"""
    res = get_list("caseList")
    project_id = get_project_id(project, res[1])
    groups = GroupApiMode.objects.filter(projectId=project_id, groupFlg=True)  # 默认下拉框数据
    group_ids = groups.values_list('id', flat=True)
    apis = ApiMode.objects.filter(apiFlg=True, groupApiId__in=group_ids)
    return render(request, "caseList_manage.html",
                  {"project": project, "products": res[0], "projects": res[1], "groups": groups, "apis": apis})


@login_required
def query_case_list(request, project):
    """列表页查询用例列表"""
    res = get_list("caseList")
    project_id = get_project_id(project, res[1])
    groups = GroupApiMode.objects.filter(projectId=project_id, groupFlg=True)  # 默认下拉框数据

    search_dic = dict()
    api_id = request.GET.get('api')
    if api_id and int(api_id) > 0:
        search_dic['apiId'] = api_id
    case_flag = request.GET.get('caseFlag')
    if case_flag:
        search_dic['caseFlag'] = case_flag
    case_env = request.GET.get('caseEnv')
    if case_env:
        search_dic['caseEnv'] = case_env
    case_level = request.GET.get('caseLev')
    if case_level:
        search_dic['caseLevel'] = case_level

    group_id = request.GET.get('apiGroup')
    if group_id and int(group_id) > 0:
        search_dic['groupApiId'] = group_id
        apis = ApiMode.objects.filter(apiFlg=True, groupApiId=group_id)
        case_lists = TestCaseMode.objects.filter(**search_dic)
    else:
        group_ids = groups.values_list('id', flat=True)
        apis = ApiMode.objects.filter(apiFlg=True, groupApiId__in=group_ids)
        case_lists = TestCaseMode.objects.filter(groupApiId__in=group_ids, **search_dic)
    return render(request, "caseList_manage.html",
                  {"project": project, "products": res[0], "projects": res[1], "groups": groups, "apis": apis,
                   "caseLists": case_lists})


@login_required
def query_api_list(request, project):
    """列表页接口下来列表"""
    group_id = int(request.GET.get('id'))
    return query_all_api(project, group_id)


@login_required
@csrf_exempt  # post请求出现403
def run_case(request, project):
    """执行用例入口"""
    _dic = dict(json.loads(request.body))
    case_ids = _dic['id']
    if case_ids.find(',') > 0:
        return run_cases(project, case_ids)
    else:
        res = run(project, case_ids)
        return HttpResponse(json.dumps({"code": "success", "mes": res[0][1]}, ensure_ascii=False),
                            content_type="application/json")


@login_required
@csrf_exempt
def case_page(request, project, pages):
    """接口用例模块页面入口"""
    res = [None, None]  # 导航数据
    groups = None  # 接口列表下拉框
    env = None  # 运行环境配置加载数据
    project_id = 0  # 用于默认值
    task_plan = None  # 任务计划详情数据
    task_id = 0
    case_info = None  # 用例详情数据
    case_id = 0
    sql_list = None  # sql语句列表数据
    api_info = None
    logs = None  # 日志列表数据
    if pages != 'runEnv':
        res = get_list("caseList")
        project_id = get_project_id(project, res[1])
    if pages == "apiList":
        groups = GroupApiMode.objects.filter(projectId=project_id)

    if pages == "apiDetail":
        groups = GroupApiMode.objects.filter(projectId=project_id)
        api_id = int(request.GET.get("id"))
        if api_id > 0:
            api_info = ApiMode.objects.get(id=api_id)

    if pages == 'runEnv':
        project_id = get_project_id(project)
        try:
            env = EnvConfigMode.objects.get(projectId=project_id)
        except Exception as e:
            print(e.__str__())
    if pages == 'taskDetail':
        task_id = int(request.GET.get("id"))
        if task_id > 0:
            task_plan = TaskPlanMode.objects.get(id=task_id)

    if pages == "caseDetail":
        case_id = int(request.GET.get("id"))
        groups = GroupApiMode.objects.filter(projectId=project_id)
        if case_id > 0:
            case_info = TestCaseMode.objects.get(id=case_id)

    if pages == "sqlList":
        api_id = int(request.GET.get("apiId"))
        api_info = ApiMode.objects.get(id=api_id)
        sql_list = ApiSqlListMode.objects.filter(apiId=api_info)

    if pages == "runLog":
        try:
            log_type = request.GET.get("logType")
            task_log_id = request.GET.get("taskLogId")
            if log_type and int(log_type) == 0:
                case_id = request.GET.get("caseId")
                case_info = TestCaseMode.objects.get(id=case_id)
                logs = CaseRunLogMode.objects.filter(caseId=case_info, logType=0)
            elif log_type and int(log_type) == 1:
                api_id = request.GET.get("apiId")
                logs = CaseRunLogMode.objects.filter(apiId=api_id, logType=1)
            elif task_log_id:
                task_log_info = TaskRunLogMode.objects.get(id=task_log_id)
                fail_log_list = list(map(int, task_log_info.failLogList.split(',')))
                logs = CaseRunLogMode.objects.filter(id__in=fail_log_list)
        except Exception as e:
            print(e.__str__())

    if pages == "taskPlanRunLog":
        task_id = request.GET.get('id')
        if task_id:
            logs = TaskRunLogMode.objects.filter(taskId=task_id)

    if pages == "userVar":
        api_id = request.GET.get("apiId")
        if int(api_id) > 0:
            api_info = ApiMode.objects.get(id=api_id)
    return render(request, pages + ".html",
                  {"project": project, "projectId": project_id, "products": res[0], "projects": res[1],
                   "groups": groups, "env": env, "taskPlanInfo": task_plan, "task_id": task_id, "caseInfo": case_info,
                   "caseId": case_id, "sqlList": sql_list, "apiInfo": api_info, "logs": logs})


def run_base_test(request, project):
    """基础测试入口"""
    try:
        _dic = dict(json.loads(request.body))
        api_id = _dic['id']
        text = run_base_case(project, api_id)
    except Exception as e:
        text = e.__str__()
    return HttpResponse(json.dumps({"result": text}, ensure_ascii=False), content_type="application/json")


def run_task_test(request, project):
    """测试计划执行入口"""
    try:
        _dic = dict(json.loads(request.body))
        task_id = _dic['id']
        _dic.pop('id')
        res = run_task(_dic, task_id, project)
        text = res[0]
    except Exception as e:
        text = e.__str__()
    return HttpResponse(json.dumps({"result": text}, ensure_ascii=False), content_type="application/json")


@csrf_exempt
def run_task_jenkins(request, task):
    """用于jenkins执行自动化测试"""
    res = ['', [0, 0, 0, [], []]]
    try:
        _dic = dict(json.loads(request.body))
        res = run_task(_dic, task)
        text = res[0]
    except Exception as e:
        text = e.__str__()
    return HttpResponse(
        json.dumps({"result": text, 'all': res[1][0], 'pass': res[1][1], 'fail': res[1][2], 'fail_list': res[1][3]},
                   ensure_ascii=False), content_type="application/json")


@login_required
@csrf_exempt
def case_page_action(request, project, pages, action):
    """接口用例模块页面操作入口"""
    if pages == "groupApiList":
        if action == "query":
            return query_group_api(request, project)
    if pages == "apiList":
        if action == "query":
            return query_api(request, project)
        if action == "runBaseTest":
            return run_base_test(request, project)
    if pages == "apiDetail":
        if action == "save":
            return save_api(request)
    if pages == "runEnv":
        if action == "save":
            return save_env(request, project)
    if pages == "taskList":
        if action == "query":
            return query_task_plan(request, project)
        if action == "runTaskTest":
            return run_task_test(request, project)
    if pages == "taskDetail":
        if action == "queryApi":
            return query_all_api(project)
        if action == "save":
            return save_task_plan(request, project)
    if pages == "caseDetail":
        if action == "save":
            return save_case(request, project)
    if pages == "sqlList":
        if action == "query":
            return query_sql_list(request)
    if pages == "userVar":
        if action == "query":
            return query_user_var_list(request, project)


def save_api(request):
    """保存接口"""
    _dic = dict(json.loads(request.body))
    api_id = int(_dic['id'])
    _dic.pop('id')
    try:
        if api_id > 0:
            api_info = ApiMode.objects.filter(id=api_id)
            api_info.update(**_dic)
        else:
            _dic['groupApiId'] = GroupApiMode.objects.get(id=_dic['groupApiId'])
            ApiMode.objects.create(**_dic)
    except Exception as e:
        return HttpResponse(json.dumps({"code": e.__str__()}), content_type="application/json")
    return HttpResponse(json.dumps({"code": "ok"}, ensure_ascii=False), content_type="application/json")


def query_user_var_list(request, project):
    """查询自定义变量列表"""
    _dict = dict()
    var_flag = request.POST.get("varFlag")
    if var_flag:
        _dict['varFlag'] = var_flag
    var_name = request.POST.get("varName")
    if var_flag:
        _dict['varName'] = var_name
    var_type = request.POST.get("varType")
    if var_type:
        _dict['varType'] = var_type
    api_id = request.POST.get("api")
    if api_id:
        _dict['apiId'] = ApiMode.objects.get(id=api_id)
    if int(var_type) != 2:  # 场景变量不需要project
        project_id = get_project_id(project)
        _dict['projectId'] = project_id
    s_id = request.POST.get("scenario")
    if s_id:
        _dict['scenarioId'] = s_id
    try:
        var_list = UserVarMode.objects.filter(**_dict)
    except Exception as e:
        return HttpResponse(json.dumps({"code": e.__str__()}), content_type="application/json")
    return HttpResponse(
        json.dumps({"code": "ok", "varList": list(var_list)}, default=lambda obj: obj.__dict__, ensure_ascii=False),
        content_type="application/json")


def query_sql_list(request):
    """查询sql列表"""
    _dict = dict()
    sql_flag = request.POST.get("apiSqlFlag")
    if sql_flag:
        _dict['apiSqlFlag'] = sql_flag
    try:
        api_id = request.POST.get("api")
        api_info = ApiMode.objects.get(id=api_id)
        sql_list = ApiSqlListMode.objects.filter(apiId=api_info, **_dict)
        res = json.loads(serializers.serialize("json", sql_list, ensure_ascii=False))
        res_list = []
        for r in res:
            new_dic = copy.deepcopy(r['fields'])
            new_dic['id'] = r['pk']
            res_list.append(new_dic)
    except Exception as e:
        return HttpResponse(json.dumps({"code": e.__str__()}), content_type="application/json")
    return HttpResponse(
        json.dumps({"code": "ok", "sqlList": res_list}, default=lambda obj: obj.__dict__, ensure_ascii=False),
        content_type="application/json")


def save_case(request, project):
    """保存接口测试用例"""
    _dic = dict(json.loads(request.body))
    case_id = int(_dic['id'])
    _dic.pop('id')
    try:
        if case_id > 0:
            case_info = TestCaseMode.objects.filter(id=case_id)
            case_info.update(**_dic)
        else:
            pro = ProjectMode.objects.get(projectTag__exact=project)
            _dic['productId'] = pro.productId.id
            _dic['projectId'] = pro.id
            _dic['apiId'] = ApiMode.objects.get(id=_dic['apiId'])
            TestCaseMode.objects.create(**_dic)
    except Exception as e:
        return HttpResponse(json.dumps({"code": e.__str__()}), content_type="application/json")
    return HttpResponse(json.dumps({"code": "ok"}, ensure_ascii=False), content_type="application/json")


def save_task_plan(request, project):
    """保存接口测试计划"""
    _dic = dict(json.loads(request.body))
    task_id = int(_dic['id'])
    _dic.pop('id')
    try:
        if task_id > 0:
            task_info = TaskPlanMode.objects.filter(id=task_id)
            task_info.update(**_dic)
        else:
            pro = ProjectMode.objects.get(projectTag__exact=project)
            _dic['projectId'] = pro
            TaskPlanMode.objects.create(**_dic)
    except Exception as e:
        return HttpResponse(json.dumps({"code": e.__str__()}), content_type="application/json")
    return HttpResponse(json.dumps({"code": "ok"}, ensure_ascii=False), content_type="application/json")


def query_all_api(project, group_id=0):
    """获取项目的有效的接口列表"""
    if group_id > 0:
        api_group = [group_id]
    else:
        project_id = get_project_id(project)
        group_list = GroupApiMode.objects.filter(projectId=project_id, groupFlg=True)
        api_group = group_list.values_list('id', flat=True)
    api_list = ApiMode.objects.filter(groupApiId__in=api_group, apiFlg=True)
    return HttpResponse(json.dumps(list(api_list), default=lambda obj: obj.__dict__, ensure_ascii=False),
                        content_type="application/json")


def query_task_plan(request, project):
    """查询任务计划列表"""
    res = get_list("caseList")
    search_dict = dict()
    project_id = request.GET.get("project")
    search_dict['projectId'] = project_id
    task_name = request.GET.get("taskPlanName")
    if task_name:
        search_dict['taskPlanName'] = task_name
    task_flag = request.GET.get("taskPlanFlag")
    if task_flag:
        search_dict['taskPlanFlag'] = task_flag
    tasks = TaskPlanMode.objects.filter(**search_dict)
    for task in tasks:
        api_list = task.taskPlanCaseApiList.split(',')
        api_list = list(map(int, api_list))
        api_obj_list = ApiMode.objects.filter(id__in=api_list)
        api_name = api_obj_list.values_list('apiName', flat=True)
        task.taskPlanCaseApiList = ','.join(api_name)
        task.taskPlanCaseLevel = task.taskPlanCaseLevel.replace('3', '核心用例').replace('2', '一般用例').replace('1', '次要用例')
    return render(request, 'taskList.html',
                  {"project": project, "projectId": project_id, "tasks": tasks, "products": res[0],
                   "projects": res[1]})


def save_env(request, project):
    """保存接口用例模块项目的执行环境"""
    _dic = dict()
    local_url = request.POST.get("localUrl")
    if local_url:
        _dic["localUrl"] = local_url
    test_url = request.POST.get("testUrl")
    if test_url:
        _dic["testUrl"] = test_url
    release_url = request.POST.get("releaseUrl")
    if release_url:
        _dic["releaseUrl"] = release_url
    product_url = request.POST.get("productUrl")
    if product_url:
        _dic["productUrl"] = product_url
    pro = ProjectMode.objects.get(projectTag=project)
    env = EnvConfigMode.objects.filter(projectId=pro.id)
    try:
        if env.count() > 0:
            env.update(**_dic)
        else:
            _dic['projectId'] = pro
            EnvConfigMode.objects.create(**_dic)
    except Exception as e:
        return HttpResponse(json.dumps({"code": e.__str__()}), content_type="application/json")
    return HttpResponse(json.dumps({"code": "ok"}), content_type="application/json")


def query_api(request, project):
    """接口维护列表查询"""
    res = get_list("caseList")
    search_dict = dict()
    project_id = request.GET.get("project")
    group_list = GroupApiMode.objects.filter(projectId=project_id)
    api_name = request.GET.get("apiName")
    if api_name:
        search_dict['apiName'] = api_name
    api_flag = request.GET.get("apiFlg")
    if api_flag:
        search_dict['apiFlg'] = api_flag
    api_group = request.GET.get("apiGroup")
    if not api_group:
        group_id_list = group_list.values_list('id', flat=True)
    else:
        group_id_list = [api_group]
    api_list = ApiMode.objects.filter(groupApiId__in=group_id_list, **search_dict)
    return render(request, 'apiList.html',
                  {"project": project, "projectId": project_id, "apis": api_list, "products": res[0],
                   "projects": res[1], "groups": group_list})


def query_group_api(request, project):
    """接口组维护查询"""
    res = get_list("caseList")
    search_dict = dict()
    group_name = request.GET.get("groupName")
    if group_name:
        search_dict['groupName'] = group_name
    group_flag = request.GET.get("groupFlg")
    if group_flag:
        search_dict['groupFlg'] = group_flag
    pro = request.GET.get("project")
    if pro:
        search_dict['projectId'] = pro
    group_list = GroupApiMode.objects.filter(**search_dict)
    return render(request, 'groupApiList.html',
                  {"project": project, "projectId": pro, "groups": group_list, "products": res[0], "projects": res[1]})


def get_project_id(project, projects=None):
    """获取项目ID"""
    project_id = 0  # 用于默认值
    if projects is not None:
        for pro in projects:
            if project == pro.projectTag:
                project_id = pro.id
    else:
        pro = ProjectMode.objects.filter(projectTag__exact=project)
        project_id = pro[0].id
    return project_id
