from apiTest.models import ApiMode, EnvConfigMode, TaskPlanMode, TestCaseMode, \
    CaseRunLogMode, TaskRunLogMode, UserVarMode, ApiSqlListMode
from projectMode.models import DBConfigMode
from django.shortcuts import HttpResponse
from projectMode.models import ProjectMode
import json
import re
import time
import requests
import itertools
# import metacomm.combinatorics.all_pairs2 as all_pairs
import copy
import dbHelper.sql as mysql
import pymssql


class ApiRequest(object):
    def __init__(self, url, _type, data, header):
        self.url = url
        self.type = _type
        self.data = data.encode('utf-8')
        self.header = header
        self.resp = self.get_resp()

    def get_resp(self):
        if self.type.upper() == 'POST':
            t = requests.post(self.url, data=self.data, headers=self.header)
        elif self.type.upper() == 'GET':
            t = requests.get(self.url, headers=self.header)
        else:
            return '暂不支持其他请求方式'
        return t


def get_data_list(_type, request_type=0):
    """
    0表示对偶算法；1表示全匹配组合
    返回参数的取值范围
    """
    if _type == 'string':
        return ["", None, "abc123"]
    elif _type == 'time':
        return ["1900-01-01", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())]
    elif _type == 'int' or _type == 0:
        return [-1, 0, 1]
    elif _type == 'decimal':
        return [-0.50, 0.0, 0.50]
    elif _type == 'bool':
        return [True, False]
    elif isinstance(_type, dict):
        if request_type == 0:
            # return dual_test_case(_type)
            pass
        elif request_type == 1:
            return itertools_case_list(_type)
    elif isinstance(_type, list):
        new_list = []
        c_list = []
        if isinstance(_type[0], dict):  # 字典集合,递归取得自己的取值范围
            if request_type == 0:
                # c_list = dual_test_case(_type[0])  # 对偶算法
                pass
            elif request_type == 1:
                c_list = itertools_case_list(_type[0])  # 全匹配算法
            for case in c_list:
                new_list.append([case])
        else:  # 数组集合
            v_list = get_data_list(_type[0])
            for case in v_list:
                new_list.append([case])
            new_list.append(v_list)  # 补全一下多个值的数组
        return new_list


def all_assemble(dic):
    """返回每个参数的取值范围组成的二维数据，用于求笛卡尔积"""
    return_list = []
    for k, v in dic.items():
        k_list = []
        for _value in get_data_list(v, 1):
            di = dict()
            di[k] = _value
            k_list.append(di)
        return_list.append(k_list)
    return return_list


def itertools_case_list(dic):
    """笛卡尔积"""
    _list = all_assemble(dic)
    case_list = []
    for item in itertools.product(*_list):
        d3 = {}
        for di in item:
            d3.update(di)
        case_list.append(d3)
    return case_list


# def dual_test_case(_base):
#     """对偶生成测试用例"""
#     if not isinstance(_base, dict):
#         return []
#     key_list = list()
#     value_list = list()
#     case_list = list()
#     for k, v in _base.items():
#         key_list.append(k)
#         value_list.append(get_data_list(v))
#     # print(key_list, value_list)
#     if value_list.__len__() >= 2:
#         res = all_pairs.all_pairs2(value_list)
#         for i, b in enumerate(res):
#             # print i, b
#             dic = dict()
#             for n in range(b.__len__()):
#                 dic[key_list[n]] = b[n]
#             case_list.append(dic)
#     else:
#         for v in value_list[0]:
#             dic = dict()
#             dic[key_list[0]] = v
#             case_list.append(dic)
#     return case_list


def create_base_case(_source):
    """设计基础测试用，空，特殊字符，超长等特殊验证"""
    return_list = []
    for k, v in _source.items():
        for _value in get_type_base_value(v):
            dic_cp2 = copy.deepcopy(_source)
            dic_cp2[k] = _value
            return_list.append(replace_default(dic_cp2))
    return return_list


def replace_default(dic):
    """替换成默认值"""
    for k, v in dic.items():
        if isinstance(v, list):
            if isinstance(v[0], dict):
                dic[k] = [replace_default(v[0])]
            else:
                dic[k] = [default_value(v[0])]
        elif isinstance(v, dict):
            dic[k] = replace_default(v)
        else:
            dic[k] = default_value(v)
    return dic


def default_value(_type):
    if _type == 'string':
        return "default_string"
    elif _type == 'time':
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    elif _type == 'int' or _type == 0:
        return 0
    elif _type == 'decimal':
        return 0.00
    elif _type == 'bool':
        return True
    else:
        return _type


def get_type_base_value(_type):
    """根据类型获取基础测试的值"""
    if _type == 'string':
        #  string类型测试，空，NULL，特殊字符，脚本，正常字符，超长字符
        return ["", None, "!@#$%^&*()_+<>?:{}|~`", "<JavaScript>alert(0)</JavaScript>", "test_string",
                "qwertyuiooasdfghjklzxcvbnmazxwsedrtfrrfugyyyfyhjjjkgughsdjgagfjdbdbsddkakdfhakjnnnnnnnnnnnnnkjguyy234567iujwertyuiosdfghjkxcvbmsdfghjkqwertyuizxcvbnasdfghjwertyui234tydfgcvdfrc c1qaz2wsx3edc4rfv5tgb6yhn7ujm8ik9ol0pqwertyuiopdfghjklzxcvbnm"]
    elif _type == 'time':
        #  时间类型测试 错误的年，月，日，非时间类值, 当前时间
        return ["0000-01-01", "1600-01-01", "2010-13-30", "2010-02-30", "not_time",
                time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())]
    elif _type == 'int' or _type == 0:
        #  整型测试 非数字类型，溢出, 0
        return ["not_int", 12567890123456781234567123451234567, -12345678912345678912345678901234567, 0]
    elif _type == 'decimal':
        #  浮点测试 非数字类型，溢出, 0
        return ["not_decimal", 12567890123456781234567123451234567.88, -12345678912345678912345678901234567.50, 0.00]
    elif _type == 'bool':
        #  布尔类型 非布尔类型, True, False
        return ["not_bool", True, False]
    else:
        #  递归
        return recursive_case(_type)


def recursive_case(_type):
    """递归,返回特殊类型的取值范围"""
    if isinstance(_type, list):
        new_list = []
        if isinstance(_type[0], dict):
            t_value_list = create_base_case(_type[0])  # 基础测试用例设计
            for t_value in t_value_list:
                new_list.append([t_value])
        else:
            for _value in get_type_base_value(_type[0]):
                new_list.append([_value])
        return new_list
    elif isinstance(_type, dict):
        return create_base_case(_type)
    else:
        return [None]


def run_cases(project, cases):
    try:
        pro = ProjectMode.objects.get(projectTag__exact=project)
        test_env = EnvConfigMode.objects.get(projectId=pro.id)
    except Exception as e:
        return HttpResponse(
            json.dumps({'code': 'success', 'result': e.__str__(), 'all': 0, 'pass': 0, 'fail': 0}, ensure_ascii=False),
            content_type="application/json")
    case_list = cases.split(',')
    res = run_cases_inner(project, case_list, test_env)
    result = "总计运行用例" + str(res[0]) + "条，其中通过" + str(res[1]) + "条；失败" + str(res[2]) + "条；"
    if res[2] > 0:
        result += "失败用例ID：" + ','.join(res[3])
    return HttpResponse(
        json.dumps({'code': 'success', 'mes': result, 'all': res[0], 'pass': res[1], 'fail': res[2]},
                   ensure_ascii=False), content_type="application/json")


def replace_vars(_str, project_id, api_info, iteration=1):
    """替换变量值"""
    var_list = re.findall(r'\$\{(.*?)\}', _str)
    var_list = list(set(var_list))  # 去重
    for _var in var_list:
        b_value = get_var_value(_var, project_id, api_info, iteration)
        if b_value is not None:
            _str = _str.replace('${' + _var + '}', str(b_value))
    return _str


def get_var_value(var_name, project_id, api_info, iteration=1):
    """获取变量值"""
    if not var_name.startswith('sql_'):  # 非sql变量
        api_var_object = UserVarMode.objects.filter(apiId=api_info, varName=var_name, varType=1)  # 优先接口变量
        if api_var_object.count() > 0:
            var_value = api_var_object[0].varValue
            return get_iteration_value(var_value, iteration)

        project_var_object = UserVarMode.objects.filter(projectId=project_id, varName=var_name,
                                                        varType=0)  # 接口变量找不到找项目全局变量
        if project_var_object.count() > 0:
            var_value = project_var_object[0].varValue
            return get_iteration_value(var_value, iteration)
    elif var_name.startswith('sql_'):  # sql变量
        sql_key = var_name.split('sql_')[1]
        sql_object = ApiSqlListMode.objects.filter(apiSqlName=sql_key, apiId=api_info)
        if sql_object.count() > 0:
            return get_sql_value(sql_object[0], iteration)
    return None


def get_iteration_value(var_value, iteration):
    """变量以逗号分隔，根据迭代次数取值"""
    try:
        var_value_list = var_value.split(",")
        if iteration <= var_value_list.__len__():  # 当前迭代次数小于参数数量时
            return var_value_list[iteration - 1]
        else:
            i = (iteration % var_value_list.__len__()) - 1  # 当前迭代次数大于参数数量时，取余
            return var_value_list[i]
    except Exception as e:
        print(e.__str__())
        return var_value


def get_sql_value(sql_object, iteration=1):
    """获取sql变量的值"""
    sql = sql_object.apiSqlNameInfo
    sql = replace_vars(sql, sql_object.projectId, sql_object.apiId, iteration)
    db_conf = sql_object.dbConfId
    try:
        db_info = DBConfigMode.objects.get(id=db_conf.id)
    except Exception as e:
        print(e.__str__())
        return None
    conf_type = int(db_info.dbType)
    _server = str(db_info.dbServer)
    ip = _server.split(',')[0]
    if _server.split(',').__len__() > 1:
        port = int(_server.split(',')[1])
    else:
        port = 80
    account = str(db_info.dbAccount)
    password = str(db_info.dbPassWord)
    db = str(db_info.dbDefault)
    if conf_type == 1:  # MySql
        ms = mysql.MYSQL(ip, account, password, db, port)
        data = ms.query(sql)
        if data:
            return data[0][0]
        return None
    elif conf_type == 2:  # SqlServer
        conn = pymssql.connect(_server, account, password, database=db)
        cursor = conn.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        conn.close()
        if data:
            return data[0][0]
        return None
    elif conf_type == 3:  # Oracle
        return None
    elif conf_type == 4:  # MongoDB
        return None
    else:
        return None


def run_base_case(project, _id):
    """执行基础测试"""
    try:
        pro = ProjectMode.objects.get(projectTag__exact=project)
        test_env = EnvConfigMode.objects.get(projectId=pro.id)
    except Exception as e:
        return e.__str__()
    try:
        api_info = ApiMode.objects.get(id=_id)
    except Exception as e:
        return e.__str__()
    # 默认使用测试环境
    url = str(test_env.testUrl).strip() + str(api_info.apiUrl).strip()
    _type = str(api_info.apiRequestType).strip()
    header2 = str(api_info.apiHeaderEsp).strip()
    header2 = replace_vars(header2, pro.id, api_info)  # 替换其中的变量值
    header = dict()
    if header2 != '':
        header = json.loads(header2)
    if api_info.apiHeader and str(api_info.apiHeader).strip() != '':
        header['Content-Type'] = str(api_info.apiHeader).strip()
    try:
        req = json.loads(str(api_info.apiDefaultRequest).strip())
    except Exception as e:
        return e.__str__() + '请确认默认请求参数维护正确'
    case_list = create_base_case(req)
    if case_list.__len__() < 1:
        return '请确认默认请求参数维护正确'
    for case in case_list:
        case = str(json.dumps(case, ensure_ascii=False))
        try:
            test_case = ApiRequest(url, _type, case, header)
            resp = test_case.resp
        except Exception as e:
            return e.__str__()
        if resp.status_code == 200:
            act_resp = resp.text.strip()
        else:
            act_resp = str(resp.status_code)
        # 插入日志
        CaseRunLogMode.objects.create(apiId=api_info.id, runResult='基础测试', actResult=act_resp,
                                      caseBody=case, projectId=pro.id, logType=1)
    return '测试完成，测试case' + str(case_list.__len__()) + '条'


def run_task(request, task_id, project=None):
    creator = '测试'
    if 'creator' in request.keys():
        creator = request['creator']
    try:
        task_info = TaskPlanMode.objects.get(id=task_id)
        api_id_list = list(map(int, task_info.taskPlanCaseApiList.split(',')))
        level_list = list(map(int, task_info.taskPlanCaseLevel.split(',')))
        env = task_info.taskPlanRun
        if project is None:
            project = task_info.projectId.projectTag
        # apis = ApiMode.objects.filter(id__in=api_id_list)
        case_list = TestCaseMode.objects.filter(apiId__in=api_id_list, caseLevel__in=level_list, caseEnv=env)
        case_id_list = case_list.values_list('id', flat=True)
        iteration = task_info.taskPlanIteration
        i = 1
        case_num = 0
        pass_num = 0
        fail_num = 0
        fail_list = []
        fail_log_list = []
        while i <= iteration:
            res = run_cases_inner(project, case_id_list, None, i)
            case_num = case_num + res[0]
            pass_num = pass_num + res[1]
            fail_num = fail_num + res[2]
            fail_list = fail_list + res[3]
            fail_log_list = fail_log_list + res[4]

            i = i + 1

        text = "总计运行用例" + str(case_num) + "条，其中通过" + str(pass_num) + "条；失败" + str(fail_num) + "条"
        fail_text = ','.join(map(str, fail_log_list))
        # 保存运行日志
        for k, v in request.items():  # jenkins调用传入的一些参数 记录下来
            text += "；" + str(k) + ':' + str(v)  # ','.join(map(str, v))
        TaskRunLogMode.objects.create(taskId=task_id, creator=creator, runCaseNum=case_num, passNum=pass_num,
                                      failNum=fail_num,
                                      result=text, failLogList=fail_text)
    except Exception as e:
        return e.__str__(), (0, 0, 0, [], [])
    return text, (case_num, pass_num, fail_num, fail_list, fail_log_list)


def run_cases_inner(project, case_list, test_env, iteration=1):
    run_num = 0
    pass_num = 0
    fail_num = 0
    fail_list = []
    fail_log_list = []
    for _id in case_list:
        res = run(project, _id, test_env, iteration)
        run_num += 1
        if res[0][0] == "pass":
            pass_num += 1
        else:
            fail_num += 1
            fail_list.append(_id)
            fail_log_list.append(res[1])
    return run_num, pass_num, fail_num, fail_list, fail_log_list


def run(project, _id, test_env=None, iteration=1):
    """执行用例主方法"""
    if not test_env:
        try:
            pro = ProjectMode.objects.get(projectTag__exact=project)
            test_env = EnvConfigMode.objects.get(projectId=pro.id)
        except Exception as e:
            return ('fail', e.__str__()), 0

    try:
        case_info = TestCaseMode.objects.get(id=_id)
    except Exception as e:
        return ('fail', e.__str__()), 0

    url1 = ''
    out_text = ''
    if case_info.caseEnv == 0 or case_info.caseEnv == 2:
        out_text = '测试环境'
        url1 = str(test_env.testUrl).strip()
    elif case_info.caseEnv == 1:
        out_text = '本地环境'
        url1 = str(test_env.localUrl).strip()
    elif case_info.caseEnv == 3:
        out_text = '预发环境'
        url1 = str(test_env.releaseUrl).strip()
    elif case_info.caseEnv == 4:
        out_text = '正式环境'
        url1 = str(test_env.productUrl).strip()

    if url1 == '':
        out_text = '请维护' + out_text + '的地址'
        return ('fail', out_text), 0

    url = url1 + str(case_info.apiId.apiUrl).strip()
    _type = str(case_info.apiId.apiRequestType).strip()
    req = str(case_info.caseBody).strip()
    req = replace_vars(req, case_info.projectId, case_info.apiId, iteration)  # 替换其中的变量值
    exp = case_info.excRule
    header2 = str(case_info.apiId.apiHeaderEsp).strip()
    header2 = replace_vars(header2, case_info.projectId, case_info.apiId, iteration)  # 替换其中的变量值
    header = dict()
    if header2 != '':
        header = json.loads(header2)
    if case_info.apiId.apiHeader:
        header['Content-Type'] = str(case_info.apiId.apiHeader).strip()
        api_id = case_info.apiId.id
    if _type.upper() == 'GET':
        url += '?' + req
    try:
        case = ApiRequest(url, _type, req, header)
        resp = case.resp
    except Exception as e:
        # 插入日志
        log = CaseRunLogMode.objects.create(apiId=api_id, caseId=case_info, runResult="fail", actResult=e.__str__(),
                                            caseBody=req, projectId=case_info.projectId, logType=0)
        return ('fail', '请求实际结果出现问题'), log.id
    if resp.status_code == 200:
        act_resp = resp.text.strip()
        test_res = check(exp, resp.text, case_info, iteration)
    else:
        act_resp = str(resp.status_code)
        test_res = ('fail', str(resp.status_code))

    # 更新用例运行记录
    case_info.actResult = act_resp
    case_info.actNum += 1
    case_info.save()
    # 插入日志
    log = CaseRunLogMode.objects.create(apiId=api_id, caseId=case_info, runResult=test_res[0], actResult=act_resp,
                                        caseBody=req, projectId=case_info.projectId, logType=0)
    return test_res, log.id


def check(expectation, reality, case_info, iteration=1):
    """比较器入口，传断言逻辑以及实际结果"""
    try:
        exp = json.loads(expectation)
        _assert = dict(exp)
        if _assert['assertType'] == 'json':
            value = _assert['assertValue']
            return json_assert(value, reality, case_info, iteration)
        elif _assert['assertType'] == 'text':
            value = _assert['assertValue']
            return text_assert(value, reality, case_info, iteration)
        else:
            return 'fail', '断言规则类型不正确'
    except Exception as e:
        return 'fail', e.__str__()


def text_assert(text, reality, case_info, iteration):
    # 处理预期文本
    tt = text['assertText']
    tt = replace_vars(tt, case_info.projectId, case_info.apiId, iteration)  # 替换其中的变量值

    text_type = text['assertTextType'].encode('utf-8')
    _type = int(text_type)
    if _type == 1:  # 1表示正则包含
        try:
            pattern = re.compile(tt)
            result = re.search(pattern, reality)
            if result:
                return 'pass', '通过'
            else:
                return 'fail', '实际结果不包含期望结果，请检查'
        except Exception as e:
            return 'fail', e.__str__()
    elif _type == 2:  # 2表示正则全字匹配
        try:
            pattern = re.compile(tt)
            result = re.match(pattern, reality)
            if result and result.end() == reality.__len__():
                return 'pass', '通过'
            else:
                return 'fail', '实际结果和期望结果不匹配，请检查'
        except Exception as e:
            return 'fail', e.__str__()
    elif _type == 3:  # 3表示substring
        try:
            if tt in reality:
                return 'pass', '通过'
            else:
                return 'fail', '实际结果不包含期望结果'
        except Exception as e:
            return 'fail', e.__str__()
    elif _type == 4:  # 4表示==
        try:
            if tt == reality:
                return 'pass', '通过'
            else:
                return 'fail', '实际结果和期望结果不一致'
        except Exception as e:
            return 'fail', e.__str__()
    else:
        return 'fail', '类型不正确'


def json_assert(json_list, reality, case_info, iteration=1):
    """json字段断言"""
    # 处理实际结果
    try:
        real_val = json.loads(reality)
    except Exception as e:
        return 'fail', e.__str__()
    # 处理预期字段
    try:
        for data in json_list:
            data_key = data['dataKey']
            data_value = data['dataValue']
            _method = data['method']
            data_method = int(_method)

            data_value = replace_vars(data_value, case_info.projectId, case_info.apiId, iteration)  # 替换变量值
            data_key = replace_vars(data_key, case_info.projectId, case_info.apiId, iteration)  # 替换变量值
            # data_value = get_data_value_logic(data_value)  # 处理特殊逻辑

            # 处理字段层级
            menu = data_key.split('.')
            _len = menu.__len__()  # 层级数
            i = 0
            _str = '_val = real_val'
            while i <= _len - 1:
                is_num = re.search(r'\[\d*\]', menu[i])  # 判断是否存在个数
                if is_num:
                    num = is_num.group()
                    _str += "['" + menu[i].split(num)[0] + "']"
                    _str += num
                else:
                    _str += "['" + menu[i] + "']"
                i += 1
            # 获取断言字段的实际值
            try:
                _locals = locals()
                exec(_str, globals(), _locals)
            except Exception as e:
                return 'fail', e.__str__()
            # 通过设定的方式，判断期望值，实际值
            is_pass = field_assert(_locals['_val'], data_value, data_method)
            if not is_pass:
                return 'fail', '字段' + data_key + '不符合预期结果；判断类型-' + str(data_method) + '期望值为' + str(
                    data_value) + ',实际值为' + str(_locals['_val'])
    except Exception as e:
        return 'fail', e.__str__()
    return 'pass', '通过'


def get_data_value_logic(data_value):
    try:
        return exec(data_value)
    except Exception as e:
        print(e)
        return data_value


def field_assert(real, exc, _type):
    if _type == 1:
        return str(real) == exc
    elif _type == 2:
        return str(real) != exc
    elif _type == 3:
        if exc in str(real):
            return True
        else:
            return False
    elif _type == 4:
        try:
            return int(real) > int(exc)
        except Exception:
            return False
    elif _type == 5:
        try:
            return int(real) < int(exc)
        except Exception:
            return False
    elif _type == 6:
        try:
            return real is True
        except Exception:
            return False
    elif _type == 7:
        try:
            return real is False
        except Exception:
            return False
    elif _type == 8:
        try:
            if exc not in str(real):
                return True
            else:
                return False
        except Exception:
            return False
    elif _type == 9:  # 值相等,统一保留2位有效数据进行比较
        try:
            r_real = round(float(real), 2)
            r_exc = round(float(exc), 2)
            if r_real == r_exc:
                return True
            else:
                return False
        except Exception:
            return False
