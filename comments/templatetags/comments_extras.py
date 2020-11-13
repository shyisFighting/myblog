from django import template
from ..forms import CommentForm

register = template.Library()

@register.inclusion_tag('comments/inclusions/_form.html',takes_context=True)
def show_comment_form(context,post,form=None):
    if form is None:
        form = CommentForm()
    return{
        'form':form,
        'post':post
    }

@register.inclusion_tag('comments/inclusions/_list.html',takes_context=True)
def show_comments(context,post):
    # 获取post对应的所有评论，可以使用：
    # Comment.objects.filter(post=post) 从comment的所用内容中获取对应文章的评论
    # 或者通过Post实例post，拿到其对应的所用comment项--comment_set
    comment_list = post.comment_set.all().order_by('-created_time')
    comment_count = comment_list.count()
    return {
        'comment_count':comment_count,
        'comment_list':comment_list,
    }