from django.shortcuts import render
from projectMode.models import ProductMode, ProjectMode, DBConfigMode
from django.contrib.auth.decorators import login_required


# Create your views here.


@login_required
def product(request):
    return render(request, 'product.html')


@login_required
def product_query(request):
    # username = request.session.get('user', '')   # 读取浏览器登录session
    search_dict = dict()
    product_name = request.GET.get("productName")
    if product_name:
        search_dict['productName'] = product_name
    product_flag = request.GET.get("productFlag")
    if product_flag:
        search_dict['productFlag'] = product_flag
    # product_module = request.GET.get("productModule")
    # if product_module:
    #     search_dict['productModule'] = product_module
    product_list = ProductMode.objects.filter(**search_dict)
    return render(request, 'product.html', {"products": product_list})


@login_required
def project(request):
    products = ProductMode.objects.filter(productFlag=True)
    return render(request, 'project.html', {"products": products})


@login_required
def project_query(request):
    # username = request.session.get('user', '')   # 读取浏览器登录session
    search_dict = dict()
    products = ProductMode.objects.filter(productFlag=True)
    project_name = request.GET.get("projectName")
    if project_name:
        search_dict['projectName'] = project_name
    project_flag = request.GET.get("projectFlag")
    if project_flag:
        search_dict['projectFlag'] = project_flag
    product_id = request.GET.get("productId")
    if product_id:
        search_dict['productId'] = product_id
    project_list = ProjectMode.objects.filter(**search_dict)
    return render(request, 'project.html', {"projects": project_list, "products": products})


@login_required
def db_conf(request):
    dbs = DBConfigMode.objects.filter(dbFlag=True)
    return render(request, 'dbConf.html', {"dbs": dbs})


@login_required
def query_db_config(request):
    """数据库配置页面查询"""
    search_dict = dict()
    db_type = request.GET.get("dbType")
    if db_type:
        search_dict['dbType'] = db_type
    db_flag = request.GET.get("dbFlag")
    if db_flag:
        search_dict['dbFlag'] = db_flag
    dbs = DBConfigMode.objects.filter(**search_dict)
    return render(request, 'dbConf.html', {"dbs": dbs})
