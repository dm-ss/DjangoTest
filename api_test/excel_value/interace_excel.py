import xlrd

book = xlrd.open_workbook("D:\WEB\autotest\project_api\backend\excel_value\shuju.xlsx")
sheet1 = book.sheet_by_index(0)

# 单据行和列取出对应单元格的信息，表格从0开始计数
A1 = sheet1.cell_value(rowx=0,colx=0)
print(A1)

# 获取整行数据
A_row = sheet1.row_values(rowx=2)
print(A_row)

# 获取整列数据,默认整行整列都是从0开始
A_col = sheet1.col_values(colx=1)
print(A_col)

# 获取整列=1从第二行3开始
A_col2 = sheet1.col_values(colx=1,start_rowx=2)
print(A_col2)

# 获取从第3行开始，2-3两列的数据(实际不包含3)
A_col3 = sheet1.row_values(2,1,3)
print(A_col3)


# 获取第二列，3-11行数据(包含11)
A_row2 = sheet1.col_values(1,2,12)
print(A_row2)

#获取单元格值类型和内容
B1 = sheet1.row_slice(2,1,12)
print(B1)

# 获取单元格数据类型
B2 = sheet1.row_types(2,1,12)
print(B2)

############################################################################3
import requests
from Common.requests import *

def post_1():
    method = 'POST'
    url = 'http://60.205.82.64:80/v1/fin/lyzd/prepay_trial'
    params = {
        "productType":"LY_CXD",
        "isLang":"HQ",
        "loanNo":"20297000000938637",
        "qudLay":"41",
        "trialFlag":"0",
        "trialType":"Z",
        "trialAmt":""
    }
    headers = {
        "Content-Type":"application/json",
        "Cache-Control":"no-cache",
        "access-identity":"5c491689f9ee43e887fb76dd8863c8a1access",
        "access-token":"49db7b81fb1144cea2bd54c8f2e9e37e"
    }

    response = http(method, url, params, headers)
    print(response)

    # response = requests.request(method=method,url=url,data=params,headers=headers)
    # print(response.text)

# post_1()

#########################################
# 我们做接口表格是把数据写到一个sheet上还是一个sheet一个接口？

# 1.读取出此接口的请求方法
# 2.读取出url
# 3.取出是否非空列数据【“0”，“是”，“否”，“是”】,遍历是否含“是”
# 4.如果=“是”的索引/个数 【】
# 5.根据索引值取出一行的2个数据【key,类型】
# 6.根据类型，赋值空值 key = ""
# 7.如果=“否”，根据类型赋值空值
# 掉request.py 报错提示信息（确认）

#    3-1 如果类型是str:
#    3-2判断是否非空；如果是否，“” 如果是“是”，“”
# 想给他提示什么呢，如果不是我们做报错的话；在哪做提示呢？

print("正式编写")
header1 = {}

# 1.读取接口名称：获取整列=1从第二行3开始
interace_name  = sheet1.col_values(colx=0,start_rowx=2)
# 去除“”
interace_name = [i for i in interace_name if i != ''][0]
print(interace_name)

# 2.读取url
interace_url = sheet1.col_values(colx=1,start_rowx=2)
interace_url = [i for i in interace_url if i != ''][0]
print(interace_url)

# 取出请求方式
interace_method = sheet1.col_values(colx=2,start_rowx=2)
interace_method = [i for i in interace_method if i != ''][0]
print(interace_method)

#总行数
rows_count = sheet1.nrows
print(rows_count)

# 获取整个接口的D-F的数值
list_all = []
start_rowx = 2
for i in range (rows_count-2):
    # 固定列数：D-F
    A_col3 = sheet1.row_values(start_rowx, 3, 6)
    start_rowx += 1
    list_all.append(A_col3)

print(list_all)


assert1 = []
data = {}
for i in list_all:
    index_list = []
    if int(i[2]) == 1:
        index_list.append(list_all.index(i))
        index_list.append(i)
        assert1.append(index_list)

    elif int(i[2]) == 0 and i[1]=="str":  #暂时先写str情况
        data[i[0]] = ""
print("assert1:%s"%assert1)
print("展示为0的data:%s"%data)



# 1.正流程
# 2.

# 所有的必填项都赋值为空
for i in assert1:
    if i[1][1] == "str": #暂时只写str
        data[i[1][0]] = ''


print("展示为0+1的data:%s"%data)
# 要不要传请求头 要不要用现有的调取方法？
response = http(interace_method, interace_url, data, header1)
print(response)

