from urllib import request
from bs4 import BeautifulSoup
from openpyxl import Workbook

# 获取数据
def get_data(i):
    url="https://movie.douban.com/top250?start="+str(i)
    headers = {
        # 'User­Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0'
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
    }
    req = request.Request(url, headers=headers)
    response = request.urlopen(req)
    if response.getcode() == 200:
        data = response.read()
        data = str(data, encoding='utf-8')
        with open('douban.html', mode='w', encoding='utf-8') as f:
            f.write(data)

# 处理数据
def handle_data(i):
    get_data(i)
    with open('douban.html', mode='r', encoding='utf-8') as f:
        html = f.read()
    bs = BeautifulSoup(html, 'html.parser')
    items=bs.select('.grid_view .item')
    result=[]
    for item in items:
        number=item.select(".pic")[0].get_text(strip=True)
        movie_name=item.select('.title')[0].get_text(strip=True)
        info=item.select('.bd p')[0].get_text(strip=True)
        score=item.select('.rating_num')[0].get_text(strip=True)
        # year=item.select('')
        print(number)
        row={
        'num':number,
        'mov_name':movie_name,
        'info':info,
        'score':score,
        }
        result.append(row)
    return result

# 保存数据
def save_data(data):
    for item in data:
        row = [item['num'], item['mov_name'], item['info'], item['score']]
        sheet.append(row)
    # 保存工作蒲
    wb.save('豆瓣评分排行榜.xlsx')


if __name__ == '__main__':
    wb = Workbook()
    sheet = wb.create_sheet('豆瓣评分', 0)
    sheet.append(['排名', '电影名', '简要信息', '评分'])
    for i in range(100):
        if i%25==0:
            # print(i)
            save_data(handle_data(i))



