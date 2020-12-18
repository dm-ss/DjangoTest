#-*-coding:utf-8-*-
import requests,json
# from public.script_function import *
import datetime,json,re,jsonpath
def echo(*args):  #不限数量的单值参数,请求链接后等到的响应信息没有转换成json格式，记录每条数据创建时间及信息；
    for i in args:
        print ("[time:{asctime}] - INFO : {message}".format(asctime=  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),message=i))

class Http:
    def __init__(self,model):
        self.model=model
    def __request(self,**kwargs):
        if self.model.lower() == "get":
            response = requests.request("get", kwargs["url"], params=kwargs["params"], headers=kwargs["headers"])
            print(response.text)
        # post的参数名要为data
        elif self.model.lower() == "put":
            # 转换成字符串传入
            params = json.dumps(kwargs["params"], ensure_ascii=False).encode()
            response = requests.request("put", kwargs["url"], data=params, headers=kwargs["headers"])
        elif self.model.lower() == "delete":
            # 转换成字符串传入
            params = json.dumps(kwargs["params"], ensure_ascii=False).encode()
            response = requests.request("delete", kwargs["url"], data=params, headers=kwargs["headers"])
        elif self.model.lower() == "postbody":
            # 转换成字符串传入
            # params = {'partnerCode': 'shtxscf', 'partnerKey': '1814a7d4535f40d89706db470146f701', 'transNo': '22',
            #         'channelCode': '8001', 'coreEnterpriseCode': '0001',
            #          'data': '[{"type": "0","companyName": "", "userName": "天蓝_1","mobile": "18245676691","cardNo": "220221199301125456","customerCode": "S755AA3"}]'}

            # print("开始")
            # print(type(kwargs["url"]))
            # print(kwargs["url"])
            # print(kwargs["params"])
            # print(kwargs["headers"])
            params = json.dumps(kwargs["params"], ensure_ascii=False).encode() #字典->字符串 ascii 字符码 + 编码（默认utf-8）；

            # print(params)
            # print("222222222222222222222222222222222222222")
            response = requests.request("post", kwargs["url"], data=params, headers=kwargs["headers"])
            # print(response)
            # print(response.json())
            # print("以上是真实的响应结果33333333333333333333333333333333333333333")

        elif self.model.lower() == "postform":
            response = requests.request("post", kwargs["url"], data=kwargs["params"], headers=kwargs["headers"])
        elif self.model.lower() == "postfile":
            response = requests.request("post", kwargs["url"], data=kwargs["params"], headers=kwargs["headers"],
                                        files=kwargs["files"])

        return response

    # 文本转换成json字符串
    def __changeJson(self,response,**kwargs):
        try:
            responseJson = json.loads(response.text)
            return responseJson
        except:
            echo(kwargs["url"], self.model, kwargs["headers"], kwargs["params"], '请求返回值为: ' + str(response.text))
            errormessage = '返回值非json格式'
            raise RuntimeError(errormessage)

    def __call__(self,fuc):
        def wrapper(*args,**kwargs):
            fuc(*args, **kwargs)
            response=self.__request(**kwargs)
            responseJson=self.__changeJson(response,**kwargs)
            return responseJson,response.status_code
        return wrapper

@Http(model="GET")
def get(url,params,headers):
    pass

@Http(model="PUT")
def put(url,params,headers):
    pass

@Http(model="DELETE")
def delete(url,params,headers):
    pass

@Http(model="POSTFORM")
def postform(url,params,headers):
    pass

@Http(model="POSTBODY")
def postbody(url,params,headers):
    pass

@Http(model="POSTFILE")
def postfile(url,params,headers,files):
    pass


def http(method,url,params,headers):
    #  1.根据请求头及请求方式进行判断
    if  method=="POST":
        if headers['Content-Type'] == 'application/json':
            method = "postbody"
            return postbody(url=url, params=params, headers=headers)
        else:
            return postform(url=url, params=params, headers=headers)

    elif  method=="GET":
        return get(url=url, params=params, headers=headers)
    elif method=="PUT":
        return put(url=url, params=params, headers=headers)
    elif method=="DELETE":
        return delete(url=url, params=params, headers=headers)

    else:
        print("输入的请求方式错误！")





    # if method=="postbody":
    #     postbody(url=url, params=params, headers=headers)

    # elif method=="get":
    #     a = get(url=url, params=params, headers=headers)
    #     print(a)
    #     return a
    # elif method=="put":
    #     put(url=url, params=params, headers=headers)
    # elif method=="delete":
    #     delete(url=url, params=params, headers=headers)
    # elif method=="postform":
    #     postform(url=url, params=params, headers=headers)




