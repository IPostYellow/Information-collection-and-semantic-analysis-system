"""信息采集与语义分析系统 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from ncaas.views import *
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index),
    path('index/',index),
    path('tencent/',TemplateView.as_view(template_name="tencent_search.html")),
    path('news_categories/', renecate),
    path('abstract_extract/', TemplateView.as_view(template_name="abstract_extract.html")),
    path('emotion_analysis/', TemplateView.as_view(template_name="emotion_analysis.html")),
    path('keywords_extract/', TemplateView.as_view(template_name="keywords_extract.html")),
    path('newscat/',news_categories),
    path('tec_search/',sinna_news_search),
]
