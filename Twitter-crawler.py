"""
Modify by WSF，XY，ZX
"""

import time

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

"""
此文件主要使用selenium来爬取Twitter特定关键词 或 特定网站 的相关数据，例如，在Twitter输入food，然后将网址copy下来至twitter_url_network.txt文件中
目前测试，可检测所有页面，并爬取姓名，用户名，时间，博文，评论数，转推数，赞，分享
"""
chrome_driver = 'chromedriver.exe'  # 谷歌浏览器启动位置
driver = webdriver.Chrome(executable_path=chrome_driver)


def connent_url(url_path):
    """
    爬取博文内容的主要函数
    :param url_path: 需要爬取内容的网址
    :return:
    """
    time.sleep(3)
    Data_List = []
    df = pd.read_csv(url_path)
    i = 0
    for url in df:
        driver.get(url=url)
        try:
            brek_flag = False
            page = 0
            # 20是往下翻取的次数，大小根据具体有可能获得到的内容数而定
            for y in range(20):
                js = 'window.scrollBy(0,1000)'  # 设置selenium往下翻的窗口大小
                driver.execute_script(js)
                html = driver.page_source
                soup = BeautifulSoup(html, 'lxml')
                # 博文主体模块
                divs = soup.find_all(
                    'div', {'class': 'css-1dbjc4n r-18u37iz', 'data-testid': 'tweet'})
                page += 1
                print('Fetching data on page {}！！！'.format(page))
                # 开始爬取
                for div in divs:
                    data_list = []
                    # 爬取名字
                    name = div.find(
                        'div', {'class': 'css-1dbjc4n r-1awozwy r-18u37iz r-dnmrzs'}).get_text()
                    data_list.append(name)
                    # 爬取用户名
                    user_name = div.find(
                        'div', {'class': 'css-1dbjc4n r-18u37iz r-1wbh5a2 r-13hce6t'}).get_text()
                    data_list.append(user_name)
                    # 爬取日期
                    date = div.find('time')
                    data_list.append(date['datetime'])
                    # 爬取博文内容
                    dd = div.find('div', {
                        'class': 'css-901oao r-18jsvk2 r-1qd0xha r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0'})
                    # 做判断，之前爬取内容时，出现了内容为空，会直接退出浏览器，因此添加了一个为空判断
                    if dd is not None:
                        content2 = dd.get_text()
                        data_list.append(str(content2).strip().replace('\n', ''))
                    # 爬取转发数，评论数，转推数，点赞数
                    s = div.find('div', {'class': 'css-1dbjc4n r-18u37iz r-1wtj0ep r-1s2bzr4 r-1mdbhws'})
                    for seg in s:
                        data_list.append(seg.get_text())
                    Data_List.append(data_list)

                    Dtimes = 0
                    if len(Data_List) > 1:
                        if Data_List[-1][2] == Data_List[-2][2]:
                            Dtimes += 1
                    if Dtimes >= 10:
                        brek_flag = True
                        break
                time.sleep(3)
                if brek_flag:
                    break
        except:
            print('当前数据获取完毕。')
        print('第 {} 个URL信息已获取完毕。'.format(i))
        i = i + 1

    driver.close()
    # 防止重复爬取数据
    Data_List_New = []
    for data in Data_List:
        if data not in Data_List_New:
            Data_List_New.append(data)
    return Data_List_New


def Save_Data(url_path):
    """
    获取数据并保存数据
    :param url_path: 需要爬取网址的文件
    """
    Data_List_New = connent_url(url_path=url_path)
    print('共爬取了 {} 条数据。'.format(len(Data_List_New)))
    # 一共8类数据
    df_Sheet = pd.DataFrame(Data_List_New, columns=[
        'name', 'user_name', 'date', 'content', 'reply', 'relay', 'agree', 'share'])

    print('Get data successfully!!!')
    # 为了方便使用，数据保存成了CSV和xlsx两种格式
    csv_path = 'Twitter_Data.csv'
    df_Sheet.to_csv(csv_path)

    excel_path = 'Twitter_Data.xlsx'
    writer = pd.ExcelWriter(excel_path)
    df_Sheet.to_excel(excel_writer=writer, sheet_name='twitter', index=None)
    writer.save()
    print('Save - successfully!!!')
    writer.close()
    print('Close - successfully!!!')


def Run():
    # 加载数据
    Save_Data(url_path='twitter_url_network.txt')


if __name__ == '__main__':
    Run()
