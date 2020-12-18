from api_test.api.getResult import *
from Common.Common_random import *

# 拼接环境信息
def data_environment_view(environment_id):
    environment_address = list(Sys_Environment.objects.filter(id=environment_id).values('address'))
    environment_desc = list(Sys_Environment.objects.filter(id=environment_id).values('env_desc'))
    environment_data = {
        'environment_id':environment_id,
        'environment_address':environment_address[0]['address'],
        'environment_desc':environment_desc[0]['env_desc']
    }
    print("环境信息拼接为%s" % environment_data)
    return environment_data

# 拼接接口信息
def data_interface_view(interfaces_id):
#     1.取认证信息
    interfaces_authentication = list(Lyzd_Interface.objects.filter(id=interfaces_id).values('authentication'))[0]['authentication']
    if interfaces_authentication == "0":
        interfaces_encryption_url = ''
        interfaces_decrypt_url = ''
    elif interfaces_authentication == "1":
        interfaces_encryption_url = list(Lyzd_Interface.objects.filter(id=interfaces_id).values('encryption'))[0]['encryption']
        interfaces_decrypt_url = list(Lyzd_Interface.objects.filter(id=interfaces_id).values('decrypt'))[0]['decrypt']
        print(interfaces_encryption_url,interfaces_decrypt_url)
    else:
        print("认证输入错误！")


#     1-1.获取接口的api
    testcases_api = [a for a in Lyzd_Interface.objects.filter(id=interfaces_id).values('interface_name_en')][0]['interface_name_en']
    print('此时的接口api为：%s'%testcases_api)

#     2.获取请求方式
    testcases_method = list(Lyzd_Interface.objects.filter(id=interfaces_id).values('requestType'))[0]['requestType']
    print('此时的接口请求方式为：%s' % testcases_method)

#  2-2 获取接口名称
    testcases_name = list(Lyzd_Interface.objects.filter(id=interfaces_id).values('interface_name_zh'))[0]['interface_name_zh']
    print("此时的接口名称为:%s"%testcases_name)

#     3.请求接口入参表
#       3-1接口参数类型 + 随机数
    testcases_param_key = list(Lyzd_Interface_Param.objects.filter(Interface_id=interfaces_id).values('param_key','param_type', 'random_number', 'random_number_type'))
    print(testcases_param_key)

    param_list_all = []
    for param_dict in testcases_param_key:
        param_list = []
        param_list.append(param_dict['param_key'])
        param_list.append(param_dict['param_type'])
        param_list.append(param_dict['random_number'])
        param_list.append(param_dict['random_number_type'])
        param_list_all.append(param_list)
    print(param_list_all)


    param_dict = {}
    for list1 in param_list_all:
        if list1[1] == '0':  # 0表示字符串
            if list1[2] == '0':  #不生成随机数
                param_dict[list1[0]] = ""
            elif list1[2] == "1":  #生成随机数
                if list1[3] == '0':  # 生成10位随机数
                    random_result = random_number_str(10)
                    param_dict[list1[0]] =  random_result

                elif list1[3] == '1':  # 生成姓名
                    pass
                elif list1[3] == '2':  # 生成idcard
                    pass
                # 此处添加多种随机数生成方式

                else:
                    print("随机数类型传值错误")
            else:
                print("随机数字段传值错误")

        elif list1[1] == '3':
            param_dict[list1[0]] = []
        #     后期完善时间类型及整数类型
        else:
            print("类型输入错误")
    print(param_dict)
    # {'accountName': '', 'accountNo': '', 'accountSign': '', 'cardNo': '', 'cardType': '', 'currency': '', 'email': '', 'interBankFlag': '', 'isOther': '', 'merchantName': '', 'merchantNo': '', 'merchantType': '', 'orderAmt': '', 'orderNo': '', 'orderNum': '', 'orderType': '', 'smsNotify': ''}

    print("111111111")



    # 3-2.转成json类型
    json_data = json.dumps(param_dict)
    print('此时的接口入参为：%s' % json_data)

#   4.请求头入参表
    testcases_header_key = list(Lyzd_Interface_Header.objects.filter(interface_id=interfaces_id).values('header_key'))
    header_key_list = []
    header_key_dict = {}
    for i in testcases_header_key:
        header_key_list.append(i['header_key'])

    for n in header_key_list:
        header_key_dict[n] = ''
    print('此时的接口请求头入参列表为：%s' % header_key_dict)


#     5.拼接接口信息
    interface_data = {}
    interface_data['interfaces_id'] = interfaces_id
    interface_data['testcases_name']  = testcases_name
    interface_data['api'] = testcases_api
    interface_data['method'] = testcases_method
    interface_data['param_data'] = json_data
    interface_data['header_key'] = header_key_dict
    interface_data['interfaces_encryption_url'] = interfaces_encryption_url
    interface_data['interfaces_decrypt_url'] = interfaces_decrypt_url
    interface_data['interfaces_authentication'] = interfaces_authentication

    content = {
        'interface_data':interface_data
    }
    print('此时的接口拼接为：%s' % content)
    return content,param_list_all,header_key_list

# 案例信息
def data_interface_cases_view(testcase_id,test_interfaces_datas,interfaces_id):
    # 1.用例表：取出测试案例名称
    testcases_case_name = list(Lyzd_Interface_Cases.objects.filter(id=testcase_id).values('case_name'))[0]['case_name']
    print("测试案例id=%s的测试案例名称为%s" % (testcase_id, testcases_case_name))

    # 2用例表：取出用例分类(数据校验，业务逻辑校验，疏通测试)
    testcases_case_type = list(Lyzd_Interface_Cases.objects.filter(id=testcase_id).values('case_type'))[0]['case_type']
    print("测试案例id=%s的测试用例分类为%s" % (testcase_id, testcases_case_type))
    if testcases_case_type == "1" or testcases_case_type == "2":

        # 3.用例表：取出校验分类（问题涉及数据库校验,后续加判断）
        testcases_check_type = list(Lyzd_Interface_Cases.objects.filter(id=testcase_id).values('check_type'))[0]['check_type']
        print("测试案例id=%s的测试案例校验分类为%s" % (testcase_id, testcases_check_type))
        print("后续补充数据库校验！！！")

        # 3.用例表：拼接校验关键字+断言类型+预期值
        testcases_check_key = list(Lyzd_Interface_Cases.objects.filter(id=testcase_id).values('check_key'))[0]['check_key']
        testcases_check_condition = list(Lyzd_Interface_Cases.objects.filter(id=testcase_id).values('check_condition'))[0]['check_condition']
        testcases_check_value = list(Lyzd_Interface_Cases.objects.filter(id=testcase_id).values('check_value'))[0]['check_value']

        list_check_key = testcases_check_key.split(",")
        list_check_condition = testcases_check_condition.split(",")
        list_check_value = testcases_check_value.split(",")

        li_list = []
        out_dict = {}

        len_check_condition = len(list_check_condition)
        for i in range(len_check_condition):
            li_dict = {}
            li_dict[list_check_condition[i]] = list_check_value[i]
            li_list.append(li_dict)

        for n in range(len(list_check_key)):
            out_dict[list_check_key[n]] = li_list[n]

        print("测试案例id=%s的测试案例校验数据为%s" % (testcase_id, out_dict))

        # 4.用例入参表取值

        param_key_dict = {}
        for n in test_interfaces_datas[1]:  # ['accountName', '0', '0', '']
            if n[2] == "0":  # 无随机数，数据库取值
                testcases_param_values = list( Lyzd_Interface_Case_Param.objects.filter(Interface_Cases_id=testcase_id, param_key=n[0]).values( 'param_value'))
                param_key_list = []
                for i in n:
                    param_key_list.append(i)
                param_key_list.append(testcases_param_values[0]['param_value'])
                # print(param_key_list)
                if param_key_list[1] == "0":
                    param_key_dict[param_key_list[0]] = param_key_list[4]
                elif param_key_list[1] == '3':
                    param_key_dict[param_key_list[0]] = eval(param_key_list[4])

            elif n[2] == "1": #有随机数
                random_values = eval(test_interfaces_datas[0]['interface_data']['param_data'])[n[0]]
                param_key_dict[n[0]] = random_values
                print("111")

        print("测试案例id=%s的测试用例入参值为%s" % (testcase_id, param_key_dict))
        print("111")


        # 5.请求头入参表：取出请求头对应的key,value
        header_key_dict = {}
        for header_key in test_interfaces_datas[2]:
            testcases_param_values = list(Lyzd_Interface_Header_Param.objects.filter(Interface_Cases_id=testcase_id, header_key=header_key).values('header_value'))
            header_key_dict[header_key] = testcases_param_values[0]['header_value']
        print("测试案例id=%s的测试用例请求头入参值为%s" % (testcase_id, header_key_dict))

        # 6.执行条件
        testcases_action_condition = list(Lyzd_Interface_Cases.objects.filter(id=testcase_id).values('action_condition'))[0]['action_condition']
        print("测试案例id=%s的执行条件为%s" % (testcase_id, testcases_action_condition))
    else:  #数据校验
        pass

    print("注意！！！！！！！！！！！！")

    # 6.测试案例拼接数据
    interface_case_data = {}
    interface_case_data['id'] = int(testcase_id)
    interface_case_data['case_name'] = testcases_case_name
    interface_case_data['case_type'] = testcases_case_type
    interface_case_data['check_type'] = testcases_check_type
    interface_case_data['action_condition'] = testcases_action_condition
    interface_case_data['header'] = header_key_dict
    interface_case_data['assert_response'] = out_dict
    interface_case_data['param_testcase_data'] = param_key_dict


    content = {
        'Querytestcases':interface_case_data
    }
    print("拼接好的案例数据为：%s"%content)
    return content

def data_view(interface_case_data,test_interfaces_datas,environment_data):
    # 1.整体拼接:接口+测试案例+环境变量
    data = []
    data.append(environment_data)
    data.append(test_interfaces_datas[0]['interface_data'])
    data.append(interface_case_data)
    print(data)
    return data


# 测试案例取值
def testcasedata_view(test_case_toll_datas):

    # 1.取出url
    url = test_case_toll_datas[0]['environment_address']+test_case_toll_datas[1]['api']
    # 2.取出方式
    request_way = test_case_toll_datas[1]['method']

    # 3.取出加密解密url
    interfaces_encryption_url = test_case_toll_datas[1]['interfaces_encryption_url']
    interfaces_decrypt_url =  test_case_toll_datas[1]['interfaces_decrypt_url']

    interfaces_authentication = test_case_toll_datas[1]['interfaces_authentication']

    # 4.取测试案例数据（测试案例id+测试案例名称+数据+校验分类+请求头+断言）
    interfaces_id = test_case_toll_datas[1]['interfaces_id']
    testcases_id = test_case_toll_datas[2]['Querytestcases']['id']
    testcases_name = test_case_toll_datas[2]['Querytestcases']['case_name']
    param_testcase_data = test_case_toll_datas[2]['Querytestcases']['param_testcase_data']
    header = test_case_toll_datas[2]['Querytestcases']['header']
    assert_response = test_case_toll_datas[2]['Querytestcases']['assert_response']

    content = {
        'interfaces_id':interfaces_id,
        'testcases_id':testcases_id,
        'testcases_name':testcases_name,
        'url':url,
        'request_way':request_way,
        'header':header,
        'assert_response':assert_response,
        'param_testcase_data': param_testcase_data,
        'interfaces_encryption_url' :interfaces_encryption_url,
        'interfaces_decrypt_url':interfaces_decrypt_url,
        'interfaces_authentication':interfaces_authentication,

    }

    return content

# 涉及到json数据传递的时候，存在嵌套，导致json数据不正确，返回值信息就不正确==>去除粘贴过来时存在的换行
# def json_data(content):
#     content = json.loads(content['testcases_datas']['data'])
#     return content


