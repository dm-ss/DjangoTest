import unittest
import logging
from django.http import HttpResponse, JsonResponse

filenumber = 0


# 断言内置方法
def getAssertWay(assertway, assert_content, response_content,assert_list):
    if assertway == "assertEqual":  # 等于
        try:
            assert assert_content == response_content
            assert_list.append(response_content)
        except:
            print("{}不相等{}".format(assert_content, response_content))
            global filenumber
            filenumber += 1
            print(response_content)
            assert_list.append(response_content)

    elif assertway == "assertNotEqual":  # 不等于
        try:
            assert assert_content != response_content
            assert_list.append(response_content)
        except:
            print("{}与{}断言错误".format(assert_content, response_content))
            filenumber += 1
            assert_list.append(response_content)

    elif assertway == "assertRegexpMatches":  # 包含
        try:
            assert assert_content in response_content
            assert_list.append(response_content)
        except:
            print("{}不包含{}".format(assert_content, response_content))
            filenumber += 1
            assert_list.append(response_content)


    elif assertway == "assertNotRegexpMatches":  # 不包含
        try:
            assert assert_content not in response_content
            assert_list.append(response_content)
        except:
            print("{}与{}包含关系断言错误".format(assert_content, response_content))
            filenumber += 1
            assert_list.append(response_content)

    elif assertway == "assertGreater":  # 大于
        try:
            assert assert_content > response_content
            assert_list.append(response_content)
        except:
            print("{}不大于{}".format(assert_content, response_content))
            filenumber += 1
            assert_list.append(response_content)

    elif assertway == "assertGreaterEqual":  # 大于等于
        try:
            assert assert_content >= response_content
            assert_list.append(response_content)
        except:
            print("{}与{}大小关系判断错误".format(assert_content, response_content))
            filenumber += 1
            assert_list.append(response_content)

    elif assertway == "assertLess":  # 小于
        try:
            assert assert_content < response_content
            assert_list.append(response_content)
        except:
            print("{}不小于{}".format(assert_content, response_content))
            filenumber += 1
            assert_list.append(response_content)

    elif assertway == "assertLessEqual":  # 小于等于
        try:
            assert assert_content <= response_content
            assert_list.append(response_content)
        except:
            print("{}与{}大小关系判断错误".format(assert_content, response_content))
            filenumber += 1
            assert_list.append(response_content)

    elif assertway == "assertIn":  # 在列表中
        try:
            assert assert_content in response_content
            assert_list.append(response_content)
        except:
            print("{}在{}中".format(assert_content, response_content))
            filenumber += 1
            assert_list.append(response_content)


    elif assertway == "assertNotIn":  # 不在列表中

        try:
            assert assert_content not in response_content
            assert_list.append(response_content)
        except:
            print("{}不在{}里面".format(assert_content, response_content))
            filenumber += 1
            assert_list.append(response_content)
    return assert_list




def carry_assert(assert_response, responseJson):
    print('预期断言数据：%s' % assert_response)
    print('实际响应数据：%s' % responseJson)
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

    assert_response_list_all = []
    for key, value in assert_response.items():
        global filenumber
        filenumber = 0

        assert_response_list = []
        assert_response_dict = {}
        assert_response_dict[key] = value
        assert_response_list.append(assert_response_dict)
        assert_response_list_all.append(assert_response_list)
        print("assert_response_list_all为：%s"%assert_response_list_all)

    for assert_list in assert_response_list_all:
        print("assert_list为：%s"%assert_list)

        for i in assert_list[0]:
            responseJson_list = list(responseJson.keys())
            print('实际响应key列表:%s' % responseJson_list)
            if i not in responseJson_list:
                filenumber += 1
                print('预期key错误，key值是%s,这条测试案例错误数量+1，此时filenumber为%d' % (i, filenumber))
                assert_list.append("")

            else:
                assertway = list(assert_list[0][i].keys())[0]
                assert_content = assert_list[0][i][assertway]
                response_content = str(responseJson[i])
                getAssertWay(assertway, assert_content, response_content,assert_list)

    return assert_response_list_all

# 每个断言条件之间的关系（and/or）
# 控制开关 且=1 或=0
# 后期传值+接口id+测试用例id 返回结果时XX接口的XX用例执行成功/失败
# 将结果直接存储到两个表中
# 待确认：目前实现得是只要开关打开，即使是没有传值就当作失败处理

def test_case_judge(assert_response):
    global filenumber
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1")
    print("filenumber:%s" % filenumber)

    # 做判断，取出来的是and(1)还是or(0)
    switch = 1
    assert_response_len = len(list(assert_response.keys()))

    if switch == 1:
        if filenumber > 0:
            print("存在断言失败的情况（且），案例执行失败")
            content = 'fail'
            return content
        else:
            print("全部断言成功，案例执行成功")
            content = 'success'
            return content

    else:
        if filenumber == assert_response_len:
            print("全部断言失败（或），案例执行失败")
            content = 'fail'
            return content

        else:
            print("断言成功，案例执行成功")
            content = 'success'
            return content



# 断言