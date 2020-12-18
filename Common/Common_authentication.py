from Common.requests import *

# 加密
def Encryption(url,method,data,header):
    ret = http(method=method, url=url,params=data, headers=header)
    encryption_responseJson = ret[0]

    return encryption_responseJson


def Decrypt(url,method,data,header):
    decrypt_ret = http(method=method, url=url,params=data, headers=header)
    decrypt_responseJson = decrypt_ret[0]

    return decrypt_responseJson

def authentication_assert(test_case_toll_datas):
    print("认证类型为：%s"%test_case_toll_datas)
    if test_case_toll_datas['interfaces_authentication'] == '0':  #无认证
        # 1.调接口
        ret = http(method=test_case_toll_datas['request_way'], url=test_case_toll_datas['url'],params=test_case_toll_datas['param_testcase_data'], headers=test_case_toll_datas['header'])
        responseJson_ret = ret[0]

    elif test_case_toll_datas['interfaces_authentication'] == '1':     #     2.有认证
        # 2-1 调加密接口
        encryption_ret = Encryption(test_case_toll_datas['interfaces_encryption_url'],test_case_toll_datas['request_way'],test_case_toll_datas['param_testcase_data'],test_case_toll_datas['header'])
        print("加密返回值:%s" % encryption_ret)

        #  2-2重新拼接用例data内容
        test_case_toll_datas['param_testcase_data'] = encryption_ret
        print("重新拼接后的案例：%s" % test_case_toll_datas)
        ret = http(method=test_case_toll_datas['request_way'], url=test_case_toll_datas['url'],params=test_case_toll_datas['param_testcase_data'],headers=test_case_toll_datas['header'])
        print("ret:%s" % ret[0])

        # 2-3  解密url,data,method,header
        responseJson_ret = Decrypt(test_case_toll_datas['interfaces_decrypt_url'],test_case_toll_datas['request_way'], ret[0],test_case_toll_datas['header'])
        print("responseJson_ret:%s" % responseJson_ret)

    return responseJson_ret