import xlrd
from Common.Common_random import *
from Common.Common_api2 import *
from Common.Common_authentication import *
from Common.assertapi import *
from Common.Common_statistics import *


# view中的regular_check_seccess_data列表中包含所有执行成功得测试案例信息；
# 一个接口对应多个测试案例，有成功有失败得，成功得测试案例也包含里面；
# 因此列表里面得接口个数会多余interface_succcess_list；interface_succcess_list列表只统计此接口下得测试案例全部成功得接口；

def  regular_check_seccess_screen(regular_check_seccess_data,interface_succcess_list):
    for i in regular_check_seccess_data:
        if i[1]['interfaces_id'] not in interface_succcess_list:
            regular_check_seccess_data.remove(i)

        else:
            pass
    return regular_check_seccess_data

# def Regular_Check(interface_succcess_list,case_type,test_case_toll_datas): #[1,2,3]
def Regular_Check(interface_succcess_list, test_case_seccess_datas):  # [1,2]
    if len(interface_succcess_list) == 0: #没有成功
        pass
    elif len(interface_succcess_list) != 0:

        print("此时成功得测试接口列表为:%s"%interface_succcess_list)
        print("成功的测试测试案例数据：%s" % test_case_seccess_datas)

        # 获取执行成功的接口名称列表
        interface_succcess_name = list_name(interface_succcess_list)
        print("成功得测试接口名称列表interface_succcess_name:%s" % interface_succcess_name)

        for test_case_toll_datas in test_case_seccess_datas:
            # 取出来接口case_type
            print("当前执行的接口是:%s"%test_case_toll_datas)

            case_type = test_case_toll_datas[2]['Querytestcases']['case_type']
            if case_type == "2":  # 疏通测试
                book = xlrd.open_workbook(r'excel_value/shuju.xlsx')
                sheet_name = book.sheet_names()  # ['Sheet1', 'Sheet2', 'Sheet3']
                for i in sheet_name:
                    sheet1 = book.sheet_by_name(i) ##先获取此页的接口名称，是否在interface_succcess_name里面
                    interace_name = sheet1.col_values(colx=0, start_rowx=2)
                    interace_name = [i for i in interace_name if i != ''][0]  # 如果合并单元格需要去除“”
                    print("接口名称为:%s"%interace_name)

                    # 补充案例
                    if interace_name in interface_succcess_name and interace_name == test_case_toll_datas[1]['testcases_name']:
                        sheet_list_all = excel_data(sheet1)
                        print("%s接口读取B-G数据：%s" % (interace_name,sheet_list_all))  # [['merchantName', 'str', '0', '', '', ''],['merchantName', 'str', '0', '', '', '']..]

                        # 必填项依次为空  独立出来
                        for list_1 in sheet_list_all:
                            if list_1[1] == "str":
                                if list_1[2] == "1":
                                    # 2-1 必填项全部生成随机数
                                    test_case_toll_datas = random_data(sheet_list_all, test_case_toll_datas)
                                    print("更新一遍必填项得总数据为test_case_toll_datas_1:%s"%test_case_toll_datas)

                                    # 2-2 依次必填项为空，并重新拼接获取测试案例
                                    testcasedata_datas = required_empty_data(list_1, test_case_toll_datas)
                                    print('重新替换预期值，拼接后的数据为:%s' % testcasedata_datas)

                                    # 2-3认证判断+调http请求
                                    responseJson_ret = authentication_assert(testcasedata_datas)
                                    print("实际response返回值为：%s" % responseJson_ret)

                                    #     2-4断言
                                    assert_response_list_all = carry_assert(testcasedata_datas['assert_response'],responseJson_ret)
                                    print("接收实际的返回结果:%s" % assert_response_list_all)

                                    # 2-5 根据断言结果统计单个案例执行结果
                                    test_case_result = test_case_judge(testcasedata_datas['assert_response'])
                                    print('此条案例id=%s的执行结果为%s' % (testcasedata_datas['testcases_id'], test_case_result))

                                    #     2-6存储结果
                                    statistics_testcase_result = statistics_interface_action_detail(testcasedata_datas['interfaces_id'],testcasedata_datas['testcases_id'],testcasedata_datas[ 'param_testcase_data'],responseJson_ret,assert_response_list_all,test_case_toll_datas[2]['Querytestcases'][ 'action_condition'])
                                    print(statistics_testcase_result)


                                else:  # 非必填项保留
                                    pass

                            else:  # 其他数据类型
                                pass



                        # 3.所有的选填项全部置空

                        # 3-1必填项全部设置为随机数
                        random_data_all = random_data(sheet_list_all, test_case_toll_datas)
                        print("此时的随机数据为：%s"%random_data_all)

                        # sheet_list_all = [['orderNo', 'str', '1', 'data', 'assertRegexpMatches', '90'],['orderNo', 'str', '0', 'data', 'assertRegexpMatches', '90']]

                        a = []
                        for i in sheet_list_all:
                            a.append(i[2])
                        print("a:%s"%a)

                        if "0" in a: #存在必填项的话
                            for param_list in sheet_list_all:  # ['currency', 'str', '0', '', '', '']
                                if param_list[1] == "str":
                                    if param_list[2] == "0":  # 非空全部置空
                                        # 3-2需填写设置为空
                                        random_data_all[2]['Querytestcases']['param_testcase_data'][param_list[0]] = ''
                                        testcasedata_datas2 = testcasedata_view(random_data_all)
                                        print("取值后的testcasedata_datas：%s" % testcasedata_datas2)
                                    else:
                                        pass

                                else:  # 其他类型
                                    pass

                            # 3-3 认证判断+调http请求
                            responseJson_ret = authentication_assert(testcasedata_datas2)
                            print("实际返回值为：%s" % responseJson_ret)

                            # 3-4
                            assert_response_list_all = carry_assert(testcasedata_datas2['assert_response'],
                                                                    responseJson_ret)
                            print("接收实际的返回结果:%s" % assert_response_list_all)

                            # 3-5
                            test_case_result = test_case_judge(testcasedata_datas2['assert_response'])
                            print('此条案例id=%s的执行结果为%s' % (testcasedata_datas2['testcases_id'], test_case_result))

                            # 3-6
                            statistics_testcase_result = statistics_interface_action_detail(
                                testcasedata_datas2['interfaces_id'],
                                testcasedata_datas2['testcases_id'],
                                testcasedata_datas2['param_testcase_data'],
                                responseJson_ret,
                                assert_response_list_all,
                                test_case_toll_datas[2]['Querytestcases']['action_condition'])

                            print(statistics_testcase_result)

                        else: #全部是必填项
                            pass

                    else:
                        print("接口执行失败，不再读取数据")
                        pass
            else: #除了疏通测试以外的类型!
                pass

    else:
        print("interface_succcess_list数据类型错误!")

def list_name(interface_succcess_list):
    interface_succcess_name = []
    for interface_succcess in interface_succcess_list:
        interface_name = list(Lyzd_Interface.objects.filter(id=interface_succcess).values('interface_name_zh'))[0][
            'interface_name_zh']
        interface_succcess_name.append(interface_name)

    return interface_succcess_name

# 读取表数据
def excel_data(sheet1):
    # 读取接口名称：获取整列A列从第三行开始
    interace_name = sheet1.col_values(colx=0, start_rowx=2)
    # 2-1 合并单元格，去除“”
    interace_name = [i for i in interace_name if i != ''][0]
    print(interace_name)

    # 总行数
    rows_count = sheet1.nrows


# 4.获取整个接口的B-G的数值
    list_all = []
    start_rowx = 2
    for i in range(rows_count - 2):
        # 固定列数：B-G
        A_col3 = sheet1.row_values(start_rowx, 1, 7)
        list_all.append(A_col3)
        start_rowx += 1

    return list_all

# =1的全部生成随机数
def random_data(list_all,test_case_toll_datas):
    for list_1 in list_all:
        if list_1[1] == "str":
            if list_1[2] == "1":
                # 给必填项全部赋值，放置存在唯一性
                test_case_toll_datas[2]['Querytestcases']['param_testcase_data'][list_1[0]] = random_number_str(2)

    return test_case_toll_datas



#遍历每一个必填项，分别为空，预期值拼接，校验，结果入库；
def  required_empty_data(list_1,test_case_toll_datas):
    print("list_1预期值与list_1_2值一样%s"%list_1)
    print("此时得test_case_toll_datas预期与test_case_toll_datas_1一样:%s"%test_case_toll_datas)

    test_case_toll_datas[2]['Querytestcases']['param_testcase_data'][list_1[0]] = ''
    testcasedata_datas = testcasedata_view(test_case_toll_datas)
    print('必填项其中一位置空，取值后的数据为:%s' % testcasedata_datas)

    #          替换预期值；从表中读取数据进行替换  {'data': {'assertEqual': '{}'}}
    list_check_dict = {}
    list_li = {}
    list_li[list_1[4]] = list_1[5]
    list_check_dict[list_1[3]] = list_li
    testcasedata_datas['assert_response'] = list_check_dict
    return testcasedata_datas












