#-*- coding:utf-8 -*-
import json
import os
import requests
from bs4 import BeautifulSoup
import urllib.request
import re
import io
import sys
from urllib.parse import quote
import codecs
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')

# 函数功能：得到网易新闻
def get163news():

    url = "http://news.163.com/rank/"  # 请求网易新闻的URL，获取其text文本
    wbdata = requests.get(url).text        # 对获取到的文本进行解析
    soup = BeautifulSoup(wbdata, 'lxml')    # 创建一个beautifulsoup对象
    news_titles = soup.select("td  a")      # 从解析文件中通过select选择器定位指定的元素，返回一个列表
    comment = soup.select("td.cBlue")  #获取网页内容的步骤对应其它网页相同，不予赘述

    # 循环链接列表将获取到的标题、时间、来源、评论、正文写进txt文件

    start = 3
    i = 30
    n = 30
    for strat in range(30,500):
        for n in range(start, start + 29):
            link = news_titles[n].get("href")
            try:
                neteasedata = urllib.request.urlopen(link).read()
                neteasedata2 = neteasedata.decode("gbk", "ignore")

                soup = BeautifulSoup(neteasedata2, "html.parser")

                content = soup.select('p')
                title = soup.select('title')
                time = soup.select('div.post_time_source')
                author = soup.select('div.post_time_source > a.ne_article_source')

                if (len(time) != 0):
                    fo = open(r"C:\Users\黄寄\Desktop\信息采集与语义分析系统\static\news\新闻\网易" + str(i) + ".txt", "w+")
                    if (len(title) != 0):
                        fo.writelines("      " + title[0].get_text().strip() + "\n")
                    fo.writelines("时间：" + time[0].get_text().strip() + "\n")
                    fo.writelines("评论数: " + comment[i].get_text() + "\n" )
                    if (len(author) != 0):
                        fo.writelines(author[0].get_text() + '\n')

                    # print(title[0].get_text())
                    # print(time[0].string)
                    # print(author[0].get_text()
                    for m in range(2, len(content)):
                        try:
                            con = content[m].get_text().strip()
                            if (len(con) != 0):
                                fo.writelines("\n" + con)

                        except Exception as err:
                            print(err)
                        m += 1
                    fo.close()
            except Exception as err:
                print(err)

            i += 1
            n += 1
        start += 60
        n = start
        i = start
        if(start > 270):
            break

# 函数功能：得到腾讯新闻首页所有新闻链接
def getQQurl():
    url = "http://news.qq.com/"

    wbdata = requests.get(url).text

    soup = BeautifulSoup(wbdata, 'lxml')

    news_titles = soup.select("div.text > em.f14 > a.linkto")

    fo = open(r"C:\Users\黄寄\Desktop\信息采集与语义分析系统\static\news\QQ链接.txt", "w+",encoding='utf-8')  # 创建TXT文件保存首页所有链接

    # 对返回的列表进行遍历
    for n in news_titles:
        title = n.get_text()
        link = n.get("href")
        fo.writelines(link + "\n")
    fo.close()


# 函数功能：根据获取的链接依次爬取新闻正文并保存到本地
def getqqtext():
    qqf = open(r"C:\Users\黄寄\Desktop\信息采集与语义分析系统\static\news\QQ链接.txt", "r",encoding='utf-8')
    qqurl = qqf.readlines()  # 读取文件，得到一个链接列表
    i = 0

    # 遍历列表，请求网页，筛选出正文信息
    for qurl in qqurl:
        try:
            data = urllib.request.urlopen(qurl).read()
            data2 = data.decode("gbk", "ignore")

            soup = BeautifulSoup(data2, "html.parser")  # 从解析文件中通过select选择器定位指定的元素，返回一个列表

            content = soup.select('p')  # 选择正文内容
            title = soup.select('title')  # 选择标题
            time = soup.select('div.a_Info > span.a_time')
            author = soup.select('div.a_Info > span.a_source')

            # 将得到的网页正文写进本地文件

            fo = open(r"C:\Users\黄寄\Desktop\信息采集与语义分析系统\static\news\新闻\腾讯" + str(i) + ".txt", "w+",encoding='utf-8')

            if (len(title) != 0):
                fo.writelines("      " + title[0].get_text().strip() + "\n")
                if(len(time)!=0):
                    fo.writelines("时间："+time[0].get_text().strip() + "\n")
                if (len(author) != 0):
                    fo.writelines("来源："+author[0].get_text() + '\n'+ "\n")

                # print(title[0].get_text())
                # print(time[0].string)
                # print(author[0].get_text()
                for m in range(0, len(content)):
                    con = content[m].get_text().strip()
                    if (len(con) != 0):
                        fo.writelines("\n" + con)
                    m += 1
                fo.close()

        except Exception as err:
            print(err)

        i += 1

#函数功能：得到搜狐新闻首页所有新闻链接
def getsohuurl():
    url = "http://news.sohu.com/"
    wbdata = requests.get(url).text
    soup = BeautifulSoup(wbdata, 'lxml')

    news_titles = soup.select("div.list16 > ul > li > a")

    fo = open(r"C:\Users\黄寄\Desktop\信息采集与语义分析系统\static\news\sohu链接.txt", "w+",encoding='utf-8')

    for n in news_titles:
        title = n.get_text()
        link = n.get("href")
        fo.writelines(link + "\n")

    fo.close()


# 函数功能：根据获取的搜狐新闻链接依次爬取新闻正文并保存到本地
def getsohutext():
    sohuf = open(r"C:\Users\黄寄\Desktop\信息采集与语义分析系统\static\news\sohu链接.txt", "r",encoding='utf-8')
    sohuurl = sohuf.readlines()
    i = 0
    for sohuu in sohuurl:
        try:
            sohudata = urllib.request.urlopen(sohuu).read()
            sohudata2 = sohudata.decode("utf-8", "ignore")

            soup = BeautifulSoup(sohudata2, "html.parser")

            content = soup.select('p')
            title = soup.select('title')
            time = soup.select('div.article-info > span.time')
            author = soup.select('div.date-source > span.original-link')

            if (len(time) != 0):
                fo = open(r"C:\Users\黄寄\Desktop\信息采集与语义分析系统\static\news\新闻\搜狐" + str(i) + ".txt", "w+",encoding='utf-8')
                if (len(title) != 0):
                    fo.writelines( "      " + title[0].get_text().strip() + "\n")
                fo.writelines("时间：" + time[0].get_text().strip() + "\n")
                fo.writelines("评论数: 0" + "\n" + "\n")
                if (len(author) != 0):
                    fo.writelines(author[0].get_text() + '\n')

                # print(title[0].get_text())
                # print(time[0].string)
                # print(author[0].get_text()
                for m in range(0, len(content)):
                    con = content[m].get_text().strip()
                    if (len(con) != 0):
                        fo.writelines("\n"  + con)
                    m += 1

                fo.close()

        except Exception as err:
            print(err)

        i += 1

#函数功能：得到新浪新闻首页所有新闻链接
def getsinaurl():
    url = ['http://top.news.sina.com.cn/ws/GetTopDataList.php?top_type=day&top_cat=qbpdpl&top_time=20180715&top_show_num=100&top_order=DESC&js_var=comment_all_data',
    'http://top.news.sina.com.cn/ws/GetTopDataList.php?top_type=day&top_cat=www_www_all_suda_suda & top_time=20180715&top_show_num=100&top_order=DESC&js_var=all_1_data01',
    'http://top.collection.sina.com.cn/ws/GetTopDataList.php?top_type=day&top_cat=wbrmzf_qz&top_time=20180715&top_show_num=10&top_order=DESC&js_var=wbrmzf_qz_1_data&call_back=showContent',
    'http://top.news.sina.com.cn/ws/GetTopDataList.php?top_type=day&top_cat=total_slide_suda&top_time=20180715&top_show_num=100&top_order=DESC&js_var=slide_image_1_data',
    'http://top.news.sina.com.cn/ws/GetTopDataList.php?top_type=day&top_cat=wbrmzfgwxw&top_time=20180715&top_show_num=10&top_order=DESC&js_var=wbrmzfgwxw_1_data&call_back=showContent',
     'http://top.news.sina.com.cn/ws/GetTopDataList.php?top_type=day&top_cat=news_china_suda&top_time=20180715&top_show_num=20&top_order=DESC&js_var=news_',
        'http://top.news.sina.com.cn/ws/GetTopDataList.php?top_type=day&top_cat=gnxwpl&top_time=20180715&top_show_num=20&top_order=DESC&js_var=news_']
    furl = open(r"C:\Users\黄寄\Desktop\信息采集与语义分析系统\static\news\sina链接1.txt", "w+",encoding='utf-8')
    fcom = open(r"C:\Users\黄寄\Desktop\信息采集与语义分析系统\static\news\sinacom.txt", "w+",encoding='utf-8')
    for u in url:
        try:
            wbdata = requests.get(u).text
            fo = open(r"C:\Users\黄寄\Desktop\信息采集与语义分析系统\static\news\sinau.txt", "w+",encoding='utf-8')

            fo.write(wbdata)
            fo.close()

            text = open(r"C:\Users\黄寄\Desktop\信息采集与语义分析系统\static\news\sinau.txt", "r",encoding='utf-8').read()
            allurl = re.findall('"url":"(.+?)",', text)
            topnum = re.findall('"top_num":"(.+?)",', text)
            print(len(allurl))
            print(len(topnum))

            for n in allurl:
                # s=n.encode ("utf-8")
                # print(s)
                furl.writelines(n + "\n")
            for n in topnum:
                fcom.writelines(n + "\n")

        except Exception as err:
            print(err)

    furl.close()
    fcom.close()
        # sinaf = codecs.open(r"C:\Users\黄寄\Desktop\信息采集与语义分析系统\static\news/sina链接1.txt", 'r', 'utf-8')

# 函数功能：根据获取的新浪新闻链接依次爬取新闻正文并保存到本地
def getsinanews():
    sinaf1 = open(r"C:\Users\黄寄\Desktop\信息采集与语义分析系统\static\news\sina链接1.txt", "r",encoding='utf-8')
    sinaf2 = open(r"C:\Users\黄寄\Desktop\信息采集与语义分析系统\static\news\sinacom.txt", "r",encoding='utf-8')
    sinaurl = sinaf1.readlines()
    sinacom = sinaf2.readlines()
    i = 0
    for surl in sinaurl:
        try:

            realurl = surl.replace('\/', '/')
            sinadata = urllib.request.urlopen(realurl).read()
            sinadata2 = sinadata.decode("utf-8", "ignore")

            soup = BeautifulSoup(sinadata2, "html.parser")

            content = soup.select('p')
            title = soup.select('title')
            time = soup.select('div.date-source > span.date')
            author = soup.select('div.date-source > a.source')
            # comments = soup.select('div.hd clearfix > span.count > em > a.comment_participatesum_p')
            # print(len(comments))
            if (len(time) != 0):
                fo = open(r"C:\Users\黄寄\Desktop\信息采集与语义分析系统\static\news\新闻\新浪" + str(i) + ".txt", "w+",encoding='utf-8')
                if (len(title) != 0):
                    fo.writelines("      " + title[0].get_text().strip() + "\n")
                    fo.writelines("时间：" + time[0].get_text().strip() + "\n")
                    fo.writelines("评论数: " + sinacom[i] )
                if (len(author) != 0):
                    fo.writelines(author[0].get_text() + '\n')

                for m in range(0, len(content)):
                    con = content[m].get_text().strip()
                    if (len(con) != 0):
                        fo.writelines("\n" + con)
                    m += 1

                fo.close()
        except Exception as err:
            print(err)

        i += 1


# def main():
#     # get163news()
#     getQQurl()
#     getqqtext()
#     getsinaurl()
#     getsinanews()
#     getsohuurl()
#     getsohutext()
#
# main()

f=open(r"C:\Users\黄寄\Desktop\信息采集与语义分析系统\static\news\新闻\新浪1.txt", "r",encoding='utf-8')
text=f.read()
print(text)