from django.shortcuts import render
from .models import Articlepost
import markdown
#引入redirect重定向模块
from django.shortcuts import render, redirect
#引入httpResponse
from django.http import HttpResponse
#引入自定义Articlepostform类
from .forms import Articlepostform
#引入User模型
from django.contrib.auth.models import User


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
    return render(request, 'article/detail.html', context)

def article_create(request): #新建文章函数
    if request.method == 'POST': #判断用户是否提交数据
        article_post_form = Articlepostform(data = request.POST) #将提交的数据赋值到表单实例中
        if article_post_form.is_valid(): #判断提交的数据是否满足模型要求
            new_article = article_post_form.save(commit=False) #保存数据但暂时不提交到数据库
            new_article.author = User.objects.get(id=1)
            new_article.save() #将新建文章保存到数据库
            return redirect("article:article_list") #完成后返回到文章列表
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    #如果用户请求数据
    else:
        article_post_form = Articlepostform() #创建表单实例
        context = {'article_post_form': article_post_form} #赋值上下文
        return render(request, 'article/create.html', context)

# 安全删除文章
def article_safe_delete(request, id):
    if request.method == 'POST':
        article = Articlepost.objects.get(id=id)
        article.delete()
        return redirect("article:article_list")
    else:
        return HttpResponse("仅允许post请求")


#修改文章函数
def article_update(request, id):
    """
    更新文章的视图函数
    通过post方法提交表单，更新title、body等
    get方法进入初始表单页面
    :param request:
    :param id:
    :return:
    """
    article = Articlepost.objects.get(id=id)
    if request.method == "POST":
        article_post_form = Articlepostform(data=request.POST)
        if article_post_form.is_valid():
            article.title = request.POST['title']
            article.body = request.POST['body']
            article.save()
            return redirect("article:article_detail", id=id)
        else:
            return HttpResponse("表单内容有误，请重新填写。")
    else:
        article_post_form = Articlepostform()
        context = {'article': article, 'article_post_form': article_post_form}
        return render(request, 'article/update.html', context)