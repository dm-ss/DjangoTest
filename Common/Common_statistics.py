from api_test.models import *

def statistics_interface_action(environment_id, interface_action, interface_succcess_list, interface_fail_list,progect_id):
    # 1.列表去重interface_succcess_list = [1, 1, 2]  interface_fail_list=[3,3,4]

    list2 = []
    list2.append(interface_succcess_list)
    list2.append(interface_fail_list)

    for i in list2:
        print(i)
        i_copy = i[:]  # 切片拷贝
        i.clear()
        for each in i_copy:
            if each not in i:
                i.append(each)

    interface_succcess_list = list2[0]
    interface_fail_list = list2[1]

    # 当一个接口多个测试案例得时候，既有执行成功又有执行失败；接口维度记录执行失败；
    for i in interface_succcess_list:
        if i in interface_fail_list:
            interface_succcess_list.remove(i)
        else:
            pass

#     2.入数据库
    Lyzd_Interface_Action.objects.create(Project_id_id=progect_id, environment_id_id=environment_id,interface_action=interface_action,interface_aciton_succcess=interface_succcess_list,interface_aciton_fail=interface_fail_list)

    return interface_succcess_list,interface_fail_list

def statistics_interface_action_detail(interfaces_id,testcase_id,param_in,param_out,http_results,action_condition):
    print("interfaces_id:%s"%interfaces_id)
    print("testcase_id:%s" % testcase_id)
    print("param_in:%s" % param_in)
    print("param_out:%s" % param_out)
    print("http_result:%s" % http_results)
    print(action_condition)
    # 本次执行的接口id+ 测试案例id + 此用例的全部的入参 + 全部的出参 + （校验关键字 + 断言分类 +预期值）+实际返回值
    for http_result in http_results:  # [{'ceshi': {'assertEqual': '100'}}, '']
        check_key = list(http_result[0].keys())[0]
        check_condition = list(http_result[0][check_key].keys())[0]
        check_value = http_result[0][check_key][check_condition]
        out_value = http_result[1]

        print(check_key)
        print(check_condition)
        print(check_value)
        print(out_value)
        Lyzd_Interface_Action_Detail.objects.create(Interface_id_id=interfaces_id, Interface_Case_id_id=testcase_id,
                                               param_in=param_in, param_out=param_out, check_key=check_key,
                                               check_condition=check_condition, check_value=check_value,
                                               out_value=out_value, action_condition=action_condition)

    return "添加成功"




















