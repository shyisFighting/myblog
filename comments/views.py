from blog.models import Post
from django.shortcuts import get_object_or_404,redirect,render
from django.views.decorators.http import require_POST
from django.contrib import messages

from .forms import CommentForm

@require_POST
def comment(request,post_pk):
    # 得到对应的文章
    post = get_object_or_404(Post, pk=post_pk)
    # request.POST 中保存了用户提交的数据
    # 用提交的数据生成一个CommentForm的实例，这样就生成一个绑定了用户评价内容的表单
    form = CommentForm(request.POST)

    # 调用form.is_valid() 方法，检查表单数据是否合法
    if form.is_valid():
        # 检查到数据合法，调用save保存到数据库
        # commit=False 的作用，仅仅利用表单数据生成comment模型实例
        comment = form.save(commit=False)
        comment.post = post
        # 将文章对应到评论之后，保存到数据库
        comment.save()

        # extra_tags可以通过信息的tags属性调用，这里让我们可以在显示时实现不同的颜色
        messages.add_message(request,messages.SUCCESS,'评论发表成功！',extra_tags='success')
        # 重新定向到post的详情页，当redirect函数接收一个模型的实例时，
        # 它会调用这个模型的get_obsolute_url方法，重新定向到该实例的url
        return redirect(post)
    context = {
        'post':post,
        'form':form,
    }
    messages.add_message(request,messages.ERROR,'评论发送失败！请修改表单中的错误重新提交。',extra_tags='danger')
    return render(request,'comments/preview.html',context=context)

