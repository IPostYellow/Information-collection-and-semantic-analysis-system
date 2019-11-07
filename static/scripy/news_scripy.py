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