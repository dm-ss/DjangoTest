import logging

from crontab import CronTab
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView

from api_test.common.api_response import JsonResponse
from api_test.common.common import record_dynamic
from api_test.models import Sys_Environment, Project,Sys_Project
from api_test.serializers import Sys_ProjectSerializer
from api_test.serializers import SysEnvironmentSerializer

logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置，这里有一个层次关系的知识点。
"""
通用 用于前端下拉显示
获取龙盈智达项目列表
GetProjectList
"""


# class project(APIView):
#     print("1.......")
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = ()
#
#     def get(self, request):
#         print("2............")
#         """
#         接口分组
#         :param request:
#         :return:
#         """
#         project_id = request.GET.get("project_id")
#         print("projectID =")
#         print(project_id)
#         # 校验参数
#         if not project_id:
#             return JsonResponse(code="999996", msg="参数有误!")
#         if not project_id.isdecimal():
#             return JsonResponse(code="999996", msg="参数有误!")
#         # 验证项目是否存在
#         try:
#             pro_data = Project.objects.get(id=project_id)
#         except ObjectDoesNotExist:
#             return JsonResponse(code="999995", msg="项目不存在!")
#         # 序列化结果
#         pro_data = ProjectSerializer(pro_data)
#         # 校验项目状态
#         if not pro_data.data["status"]:
#             return JsonResponse(code="999985", msg="该项目已禁用")
#         # 查找项目下所有接口信息，并按id排序，序列化结果
#         obi = ApiGroupLevelFirst.objects.filter(project=project_id).order_by("id")
#         serialize = ApiGroupLevelFirstSerializer(obi, many=True)
#         return JsonResponse(data=serialize.data, code="999999", msg="成功!")

class project(APIView):
    print("进入分组列表下拉框后台方法")
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = ()


    def get(self, request):
        print("1:get 方法")
        """
        获取用例分组
        :return:
        """

        #pro_data = Project.objects.get()
        pro_data=Sys_Project.objects.filter()#filter()
        print(pro_data)

        serialize = Sys_ProjectSerializer(pro_data,many=True)
        # obi = AutomationGroupLevelFirst.objects.filter(project=project_id)
        # serialize = AutomationGroupLevelFirstSerializer(obi, many=True)
        print(serialize)

        return JsonResponse(data=serialize.data, code="999999", msg="成功！")
