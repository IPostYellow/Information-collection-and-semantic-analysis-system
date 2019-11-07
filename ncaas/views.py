from django.shortcuts import render
from static.CNN.predict import CnnModel
from static.scripy.news_scripy import getsinaurl,getsinanews
from pathlib import Path
from package.paginator import getPages  # 导入文件夹的分页通用方法
# Create your views here.

def index(request):
    return render(request, 'home.html')

def renecate(request):
    return render(request,'news_categories.html')
def news_categories(request):
    newsmessage_categories=request.POST.get('newscate')
    cnn_model = CnnModel()
    predict=cnn_model.predict(newsmessage_categories)
    return render(request,'message_show.html',{'msg':predict})

def sinna_news_search(request):
    # getsinaurl()
    # getsinanews()
    news_list=[]
    for i in range(300):
        filepath='C:\\Users\\黄寄\\Desktop\\信息采集与语义分析系统\\static\\news\\新闻\\新浪' + str(i+1) + '.txt'
        my_file = Path(filepath)
        if my_file.exists():
            f=open(filepath, "r",encoding='utf-8')
            cache=f.read()
            news_list.append(cache)

    current_page = request.GET.get("page", 1)
    pages, data = getPages(request, news_list)  # 分页处理
    return render(request, 'news_show.html', {'data': data,'pages':pages,'news':news_list})

