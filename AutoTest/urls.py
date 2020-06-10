"""TestPlat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from publicMode import views
from apiTest import caseviews
from projectMode import projectViews
# from webTest import webTestViews
# from testTools import testToolsViews
# from scenarioMode import views as scenarioViews


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login),
    path('', views.login),
    path('logout/', views.logout),
    path('home/', views.home),
    path('caseList/', caseviews.case_entry),
    path('dbConf/', projectViews.db_conf),
    path('dbConf/query', projectViews.query_db_config),
    path('product/', projectViews.product),
    path('queryProduct/', projectViews.product_query),
    path('project/', projectViews.project),
    path('queryProject/', projectViews.project_query),
    path('caseList/<project>', caseviews.case_list),
    path('caseList/<project>/query', caseviews.query_case_list),
    path('caseList/<project>/queryApiList', caseviews.query_api_list),
    path('caseList/<project>/runCase', caseviews.run_case),
    path('caseList/<project>/<pages>', caseviews.case_page),
    path('caseList/<project>/<pages>/<action>', caseviews.case_page_action),
    path('runTaskForJenkins/<task>', caseviews.run_task_jenkins),

    # path('webTest/', webTestViews.web_case_entry),
    # path('webTest/<project>', webTestViews.web_case_list),
    # path('webTest/<project>/<pages>', webTestViews.web_case_page),
    # path('webTest/<project>/<pages>/<action>', webTestViews.web_page_action),

    # path('testTool/', testToolsViews.web_main),
    # path('testTool/download', testToolsViews.download_app),
    # path('testTool/download/<project>', testToolsViews.download_app),
    # path('testTool/download/<project>/<filename>', testToolsViews.download),

    # path('testTool/job', testToolsViews.job),
    # path('testTool/job/<action>', testToolsViews.job_action),

    # path('testTool/order', testToolsViews.create_order),
    # path('testTool/order/<project>', testToolsViews.create_order),
    # path('testTool/order/<project>/query', testToolsViews.get_mac_list),
    # path('testTool/order/<project>/code', testToolsViews.get_order_code),
    # path('testTool/order/<project>/opePay', testToolsViews.ope_pay),

    # path('testTool/md5', testToolsViews.jia_mi),
    # path('testTool/md5/encrypt', testToolsViews.encrypt),

    # path('scenario/', scenarioViews.scenario_main),
    # path('scenario/<pro>', scenarioViews.scenario_main),
    # path('scenario/<pro>/queryScenario', scenarioViews.query_list),
    # path('scenario/<pro>/userVar', scenarioViews.scenario_var)
]
