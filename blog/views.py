from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Post,Category
import markdown
import re
from markdown.extensions.toc import TocExtension
from django.utils.text import slugify


# request是django为我们封装好的http请求，他是HttpRequest的一个实例

def index(request):
   # # 返回一个HttpResponse的一个实例
   # return HttpResponse('欢迎访问我的博客首页！')

   # render根据我们传入的参数构造HttpResponse实例
   # -created_time 中的'-'表示用逆序排序
   post_list = Post.objects.all().order_by('-created_time')
   return render(request, 'blog/index.html', context={'post_list':post_list
   })

def detail(request, pk):
   post = get_object_or_404(Post, pk=pk)
   # post.body = markdown.markdown(post.body,extensions=[
   #    'markdown.extensions.extra',
   #    'markdown.extensions.codehilite',
   #    'markdown.extensions.toc'
   # ])     直接实例化markdown文本
   md = markdown.Markdown(extensions=[
      'markdown.extensions.extra',
      'markdown.extensions.codehilite',
      'markdown.extensions.toc',
       TocExtension(slugify=slugify)])   # 实例化一个对象
   post.body = md.convert(post.body)  # 将文本解析为html，且生成了该文本的目录
   m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S).group(1)
   post.toc = md.toc if m is not '' else None   # 为post增添一个属性，将目录赋给它，然后在detail中渲染它,toc是html代码
   return render(request, 'blog/detail.html', context={'post':post})

def archive(request,year,month):
   post_list = Post.objects.filter(created_time__year=year,created_time__month=month   # django的参数列表要求将.改为__
                                   ).order_by('-created_time')
   return render(request,'blog/index.html',context={'post_list': post_list})

def category(request,pk):
   cate = get_object_or_404(Category,pk = pk)
   post_list = Post.objects.filter(category=cate).order_by('-created_time')
   return render(request,'blog/index.html',context={'post_list':post_list})