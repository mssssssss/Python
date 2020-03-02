# 使用urllib模块模拟浏览器发送请求
from urllib import request

from bs4 import BeautifulSoup
import pymysql

from openpyxl import Workbook

#获取数据
def get_data():
    #指定url
    url = 'https://search.51job.com/list/070200,000000,0000,00,9,99,java%25E5%25BC%2580%25E5%258F%2591,2,1.html'
    #指定请求头header
    headers = {
        # 'User­Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0'
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
    }
    req = request.Request(url, headers=headers)
    response = request.urlopen(req)
    # print(type(response))
    print(response.getcode())  #响应状态码
    # print(response.info())
    if response.getcode() == 200:
        data = response.read()  #读取出数据
        # print(type(data))
        data = str(data, encoding='gbk')  #转换为字符串
        # print(data)

        #将数据写入文件中
        with open('index.html', mode='w', encoding='gbk') as f:
            f.write(data)

#处理数据
def handle_data():
    with open('index.html', mode='r', encoding='gbk') as f:
        html=f.read()

    #创建BeautifulSoup对象
    bs=BeautifulSoup(html,'html.parser') #使用html解析器

    #查找数据
    #1. find() 查找第一个div
    # div=bs.find('div')
    # print(div)
    # print(type(div))  #Tag类型

    #2. find_all()方法 查找所有的div
    # metas=bs.find_all('meta')
    # print(type(metas))  #集合类型
    # print(metas[0])
    # print(bs.find_all(class_='language'))  #集合类型

    #3. select()方法 使用css选择器来获取元素
    # 返回的是集合类型 []
    # print(bs.select('.language'))
    # print(bs.select('#languagelist'))
    # print(bs.select('[title]'))  #有titles属性的

    #4. get_text()方法 获取tag中的文本
    # t=bs.select('.rlk')[0].get_text().strip()  #strip()：去除字符串中的空格
    # t=bs.select('.rlk')[0].get_text(strip=True)  #默认strip为False
    # print(len(t))
    # print(t)

    #获取职位的信息
    dvs=bs.select('#resultList .el')
    result=[]
    for dv in dvs[1:]: #第一个元素不遍历
        #职位名
        employee=dv.select('.t1')[0].get_text(strip=True)
        # 公司名
        company = dv.select('.t2')[0].get_text(strip=True)
        #地址
        addr = dv.select('.t3')[0].get_text(strip=True)
        #薪资
        salary = dv.select('.t4')[0].get_text(strip=True)
        # 发布日期
        pub = dv.select('.t5')[0].get_text(strip=True)
        # print(employee,company,addr,salary,pub)
        row={
            'employee':employee,
            'company':company,
            'addr':addr,
            'salary':salary,
            'pub':pub
        }
        result.append(row)
    return result

#存储到数据库中 ...未完成
# def sava_data_db(data):
#     config={
#         'host':'localhost',
#         'port':3306,
#         'user':'root',
#         'password':'',
#         'database':'py',
#         'charset':'utf8'
#     }
#     conn=pymysql.connect(**config)
#     cursor=conn.cursor()

#存储到excel表中
def sava_data_ex(data):
    wb=Workbook()
    sheet=wb.create_sheet('南京招聘信息',0)
    sheet.append(['职位名','公司名','工作地点','薪资','发布时间'])
    for item in data:
        row=[item['employee'],item['company'],item['addr'],item['salary'],item['pub']]
        sheet.append(row)

     #保存工作蒲
    wb.save('job.xlsx')

if __name__ == '__main__':
    # get_data()
    # print(handle_data())
    sava_data_ex(handle_data())
