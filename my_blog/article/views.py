from django.shortcuts import render
from .models import Articlepost
import markdown


def article_list(request): #文章列表函数
    articles = Articlepost.objects.all()
    context = {'articles': articles}
    return render(request, 'article/list.html', context)



def article_detail(request, id): #文章详情函数
    article = Articlepost.objects.get(id=id)

    #将Markdown语法渲染成html样式
    article.body = markdown.markdown(article.body,
                                     extensions=[
                                         'markdown.extensions.extra',
                                         'markdown.extensions.codehilite',
                                     ])
    context = {'article':article}
    return render(request , 'article/detail.html',context)