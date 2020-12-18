from django.http import HttpResponse
from django.shortcuts import render
# Create your views here.
import uuid
# from execute.models import *
# from common.Common_task import *
from api_test.models import *
from Common.Common_task import *
from Common.requests import *
# from common.Common_api import *
from Common.assertapi import *
from Common.Common_api2 import *
from rest_framework.views import APIView
from django.views.generic import View
from Common.Common_statistics import *
from Common.Common_authentication import *
from Common.Common_fields_check import *

"""
        新思路前提:  http://127.0.0.1:8000/project/autotestapi/
        1.已知项目id=1；
        2.选择的环境已确定;
        3.接口执行表中已知被勾选接口id为1，2 ；interface_action=[1,2]
        4.已知常规校验执行=0； 业务执行=1 （常规校验时，只支持一个接口对应一条疏通测试案例）


"""

progect_id = 1
environment_id = 1
interface_action = [1,2]
interface_succcess_list = []
interface_fail_list = []
teascase_pass = 0
teascase_fail = 0
execute = 0
regular_check_seccess_data = []



class getResult(APIView):
    print("gaojingyu-------数据迁移")

    def get(self, request):
        if execute == 0:
            statistics_interface_result = self.autotestapis_views()

            global regular_check_seccess_data
            regular_check_seccess_data = regular_check_seccess_screen(regular_check_seccess_data, statistics_interface_result[0])
            print("接口成功的测试案例为：%s"%regular_check_seccess_data)


            # Regular_Check(statistics_interface_result[0], self.test_case_toll_datas[2]['Querytestcases']['case_type'],self.test_case_toll_datas)
            Regular_Check(statistics_interface_result[0],regular_check_seccess_data)
            return JsonResponse({"code": "999999", "msg": "常规校验执行成功"})

        elif execute == 1:
            self.autotestapis_views()
            print("regular_check_seccess_data:%s"%regular_check_seccess_data)
            return JsonResponse({"code": "999999", "msg": "业务逻辑执行成功"})

        else:
            print("取消")


        # 批量执行多接口
    def autotestapis_views(self, *args, **kwargs):

        # 1.获取测试环境信息
        self.environment_data = data_environment_view(environment_id)

        # 2.已知勾选需要执行的接口id
        for self.interfaces_id in interface_action:
            global teascase_pass, teascase_fail
            teascase_pass = 0
            teascase_fail = 0

            # 3.取接口信息拼接
            self.test_interfaces_datas = data_interface_view(self.interfaces_id)
            print("id为%s的接口拼接信息为%s" % (self.interfaces_id, self.test_interfaces_datas[0]))

            # 4.调用测试案例视图函数
            self.autotestapi_views(self.interfaces_id, self.test_interfaces_datas, self.environment_data)

            #    6-1 接口统计
        self.statistics_interface_result = statistics_interface_action(environment_id, interface_action, interface_succcess_list, interface_fail_list,progect_id)
        print("添加接口执行表成功！项目id=%s,执行环境id=%s,一共执行接口：%s,执行成功的接口为：%s,执行失败的接口为:%s" % ( progect_id, environment_id, interface_action, self.statistics_interface_result[0], self.statistics_interface_result[1]))

        return self.statistics_interface_result

    #     测试案例视图
    def autotestapi_views(self, *args, **kwargs):
        # 1.已知接口id,获取此接口下的测试案例
        testcases = list(Lyzd_Interface_Cases.objects.filter(Interface_id=self.interfaces_id).values('id'))
        for testcases_id in testcases:
            testcase_id = testcases_id['id']
            print(testcase_id)

            # 2.取测试案例信息{测试案例的全部信息
            test_case_datas = data_interface_cases_view(testcase_id, self.test_interfaces_datas, self.interfaces_id)
            print("id为%s的测试案例信息为%s" % (testcase_id, test_case_datas))

            # 3.整合信息（环境+接口+案例）
            self.test_case_toll_datas = data_view(test_case_datas, self.test_interfaces_datas, self.environment_data)
            print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
            print('接口id=%s下的测试案例id=%s,整合后的测试案例信息为%s' % (self.interfaces_id, testcase_id, self.test_case_toll_datas))
            # 4.取值
            self.testcasedata_datas = testcasedata_view(self.test_case_toll_datas)
            print('取值后的数据为:%s' % self.testcasedata_datas)

            # 5.案例执行；
            http_result = self.httpapi_views(self.testcasedata_datas)

            #     6-2 测试案例统计
            statistics_testcase_result = statistics_interface_action_detail(self.interfaces_id, testcase_id, test_case_datas['Querytestcases'][ 'param_testcase_data'],self.responseJson, http_result, test_case_datas['Querytestcases'][ 'action_condition'])
            print(statistics_testcase_result)

    def httpapi_views(self, *args, **kwargs):
        try:
            # 1.根据接口认证判断
            if self.testcasedata_datas['interfaces_authentication'] == "0":
                # 1.调接口
                ret = http(method=self.testcasedata_datas['request_way'], url=self.testcasedata_datas['url'],params=self.testcasedata_datas['param_testcase_data'],headers=self.testcasedata_datas['header'])
                self.responseJson = ret[0]

            elif self.testcasedata_datas[ 'interfaces_authentication'] == "1":  # 有认证 request_way param_testcase_data header
                #     1-1调加密接口
                encryption_ret = Encryption(self.testcasedata_datas['interfaces_encryption_url'],
                                            self.testcasedata_datas['request_way'],
                                            self.testcasedata_datas['param_testcase_data'],
                                            self.testcasedata_datas['header'])
                print("加密返回值:%s" % encryption_ret)

                #  1-2重新拼接用例data内容
                self.testcasedata_datas['param_testcase_data'] = encryption_ret
                print("重新拼接后的案例：%s" % self.testcasedata_datas)
                ret = http(method=self.testcasedata_datas['request_way'], url=self.testcasedata_datas['url'],
                           params=self.testcasedata_datas['param_testcase_data'],
                           headers=self.testcasedata_datas['header'])
                print("ret:%s" % ret[0])

                # 1-3  解密url,data,method,header
                self.responseJson = Decrypt(self.testcasedata_datas['interfaces_decrypt_url'],
                                            self.testcasedata_datas['request_way'], ret[0],
                                            self.testcasedata_datas['header'])
                print("decrypt_ret:%s" % self.responseJson)

            # 2.断言
            assert_response_list_all = carry_assert(self.testcasedata_datas['assert_response'], self.responseJson)
            print("接收实际的返回结果:%s" % assert_response_list_all)

            # 3.根据断言结果统计单个案例执行结果
            test_case_result = test_case_judge(self.testcasedata_datas['assert_response'])
            print('此条案例id=%s的执行结果为%s' % (self.testcasedata_datas['testcases_id'], test_case_result))

            #   4.根据接口统计执行结果
            if test_case_result == 'success':
                global teascase_pass,regular_check_seccess_data
                teascase_pass += 1
                print('此接口id=%s成功的测试案例数量为：%s' % (self.testcasedata_datas['interfaces_id'], teascase_pass))
                interface_succcess_list.append(self.testcasedata_datas['interfaces_id'])
                print("接口执行成功的列表：%s" % interface_succcess_list)

                # 接口测试案例执行成功得信息进行存储；为了常规校验传参做准备；[id,self.test_case_toll_datas]
                # 因为常规校验针对得是一个接口对应一个疏通测试；如果一个接口对应多个疏通测试时，不支持
                regular_check_seccess_data.append(self.test_case_toll_datas)
                return assert_response_list_all

            else:
                global teascase_fail
                teascase_fail += 1
                print('此接口id=%s失败的测试案例数量为：%s' % (self.testcasedata_datas['interfaces_id'], teascase_fail))
                interface_fail_list.append(self.testcasedata_datas['interfaces_id'])
                print("接口执行失败的列表：%s" % interface_fail_list)
                return assert_response_list_all



        except Exception as e:
            # print("接口没有链接上,此接口id=%s失败的测试案例数量为：%s" % (self.interfaces_id, teascase_fail))
            print("结束啦！！！！！！！！！！！！！！")






















