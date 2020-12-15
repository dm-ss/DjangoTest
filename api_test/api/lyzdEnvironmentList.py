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
from api_test.models import Sys_Environment, Project
# from api_test.serializers import ProjectSerializer, ProjectDeserializer, \
#     ProjectMemberDeserializer
from api_test.serializers import SysEnvironmentSerializer

logger = logging.getLogger(__name__)  # 这里使用 __name__ 动态搜索定义的 logger 配置，这里有一个层次关系的知识点。
"""
龙盈智达环境列表
"""

class LyzdEnvironmentList(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def get(self, request):
        """
        获取项目列表
        :param request:
        :return:
        """
        try:
            page_size = int(request.GET.get("page_size", 20))
            page = int(request.GET.get("page", 1))

        except (TypeError, ValueError):
            return JsonResponse(code="999985", msg="page and page_size must be integer!")

        env_desc = request.GET.get("env_desc")


        if env_desc:
            obi = Sys_Environment.objects.filter(env_desc__contains=env_desc).order_by("id")

        else:

            obi = Sys_Environment.objects.all().order_by("id")

        paginator = Paginator(obi, page_size)  # paginator对象
        total = paginator.num_pages  # 总页数

        try:

            obm = paginator.page(page)

        except PageNotAnInteger:

            obm = paginator.page(1)
        except EmptyPage:

            obm = paginator.page(paginator.num_pages)
        serialize = SysEnvironmentSerializer(obm, many=True)

        # json_data = serializers.serialize("json", obm, ensure_ascii=False)
        return JsonResponse(data={"data": serialize.data,
                                  "page": page,
                                  "total": total
                                  }, code="999999", msg="成功")

#
class AddEnvironment(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()


    def parameter_check(self, data):
        """
        验证参数
        :param data:
        :return:
        """
        try:
            # 必传参数 name, version, type
            if not data["env_desc"] or not data["address"] or not data["content"]:
                return JsonResponse(code="999996", msg="参数有误！")

        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")



    def post(self, request):
        """
        新增环境
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        data["user"] = request.user.pk
        environment_serializer = SysEnvironmentSerializer(data=data)
        try:
            Sys_Environment.objects.get(env_desc=data["env_desc"])

            return JsonResponse(code="999997", msg="存在相同名称")
        except ObjectDoesNotExist:
            with transaction.atomic():
                if environment_serializer.is_valid():
                    # 保持新项目
                    environment_serializer.save()
                    # 记录动态


                    return JsonResponse(data={
                            "environment_id": environment_serializer.data.get("id")
                        }, code="999999", msg="成功")
                else:
                    return JsonResponse(code="999998", msg="失败")

#
class UpdateEnvironment(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = ()


    def parameter_check(self, data):
        """
        校验参数
        :param data:
        :return:
        """
        try:
            # 校验project_id类型为int
            if not isinstance(data["id"], int):
                return JsonResponse(code="999996", msg="参数有误！")
            # 必传参数 name, version , type
            if not data["env_desc"] or not data["address"] or not data["content"]:
                return JsonResponse(code="999996", msg="参数有误！")
            # # type 必为Web， App
            # if data["type"] not in ["Web", "App"]:
            #     return JsonResponse(code="999996", msg="参数有误！")
        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    def post(self, request):
        """
        修改项目
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        # 查找项目是否存在
        try:
            obj = Sys_Environment.objects.get(id=data["id"])
            if not request.user.is_superuser and obj.user.is_superuser:
                return JsonResponse(code="999983", msg="无操作权限！")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")
        # 查找是否相同名称的项目
        environment_name = Sys_Environment.objects.filter(env_desc=data["env_desc"]).exclude(id=data["id"])
        if len(environment_name):
            return JsonResponse(code="999997", msg="存在相同名称")
        else:
            #environment_serializer = SysEnvironmentSerializer(data=data)
            serializer = SysEnvironmentSerializer(data=data)
            with transaction.atomic():
                if serializer.is_valid():
                    # 修改项目
                    serializer.update(instance=obj, validated_data=data)
                    # 记录动态
                    record_dynamic(project=data["id"],
                                   _type="修改", operationObject="环境列表", user=request.user.pk, data=data["env_desc"])
                    return JsonResponse(code="999999", msg="成功")
                else:
                    return JsonResponse(code="999998", msg="失败")

"""
DelEnvironment,删除环境
"""
class DelEnvironment(APIView):

    authentication_classes = (TokenAuthentication,)
    permission_classes = ()

    def parameter_check(self, data):
        """
        校验参数
        :param data:
        :return:
        """
        try:
            # 校验project_id类型为int
            if not isinstance(data["ids"], list):
                return JsonResponse(code="999996", msg="参数有误！")
            for i in data["ids"]:
                if not isinstance(i, int):
                    return JsonResponse(code="999996", msg="参数有误！")
        except KeyError:
            return JsonResponse(code="999996", msg="参数有误！")

    def post(self, request):
        """
        删除项目
        :param request:
        :return:
        """
        data = JSONParser().parse(request)
        result = self.parameter_check(data)
        if result:
            return result
        try:
            for i in data["ids"]:
                try:
                    obj = Sys_Environment.objects.get(id=i)
                    if not request.user.is_superuser and obj.user.is_superuser:
                        return JsonResponse(code="999983", msg=str(obj)+"无操作权限！")
                except ObjectDoesNotExist:
                    return JsonResponse(code="999995", msg="项目不存在！")
            for j in data["ids"]:
                obj = Sys_Environment.objects.filter(id=j)
                obj.delete()
                # my_user_cron = CronTab(user=True)
                # my_user_cron.remove_all(comment=j)
                # my_user_cron.write()
            return JsonResponse(code="999999", msg="成功")
        except ObjectDoesNotExist:
            return JsonResponse(code="999995", msg="项目不存在！")


# class DisableProject(APIView):
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = ()
#
#     def parameter_check(self, data):
#         """
#         校验参数
#         :param data:
#         :return:
#         """
#         try:
#             # 校验project_id类型为int
#             if not isinstance(data["project_id"], int):
#                 return JsonResponse(code="999996", msg="参数有误！")
#         except KeyError:
#             return JsonResponse(code="999996", msg="参数有误！")
#
#     def post(self, request):
#         """
#         禁用项目
#         :param request:
#         :return:
#         """
#         data = JSONParser().parse(request)
#         result = self.parameter_check(data)
#         if result:
#             return result
#         # 查找项目是否存在
#         try:
#             obj = Project.objects.get(id=data["project_id"])
#             if not request.user.is_superuser and obj.user.is_superuser:
#                 return JsonResponse(code="999983", msg=str(obj) + "无操作权限！")
#             obj.status = False
#             obj.save()
#             record_dynamic(project=data["project_id"],
#                            _type="禁用", operationObject="项目", user=request.user.pk, data=obj.name)
#             return JsonResponse(code="999999", msg="成功")
#         except ObjectDoesNotExist:
#             return JsonResponse(code="999995", msg="项目不存在！")
#
#
# class EnableProject(APIView):
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = ()
#
#     def parameter_check(self, data):
#         """
#         校验参数
#         :param data:
#         :return:
#         """
#         try:
#             # 校验project_id类型为int
#             if not isinstance(data["project_id"], int):
#                 return JsonResponse(code="999996", msg="参数有误！")
#         except KeyError:
#             return JsonResponse(code="999996", msg="参数有误！")
#
#     def post(self, request):
#         """
#         启用项目
#         :param request:
#         :return:
#         """
#         data = JSONParser().parse(request)
#         result = self.parameter_check(data)
#         if result:
#             return result
#         # 查找项目是否存在
#         try:
#             obj = Project.objects.get(id=data["project_id"])
#             if not request.user.is_superuser and obj.user.is_superuser:
#                 return JsonResponse(code="999983", msg=str(obj) + "无操作权限！")
#             obj.status = True
#             obj.save()
#             record_dynamic(project=data["project_id"],
#                            _type="禁用", operationObject="项目", user=request.user.pk, data=obj.name)
#             return JsonResponse(code="999999", msg="成功")
#         except ObjectDoesNotExist:
#             return JsonResponse(code="999995", msg="项目不存在！")
