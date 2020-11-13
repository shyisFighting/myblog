from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.utils.html import strip_tags
import markdown
class Category(models.Model):
    name = models.CharField(max_length = 100)
    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=100)
    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Post(models.Model):

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-created_time','title']

    title = models.CharField('标题', max_length=70)
    body = models.TextField('正文')
    auto_excerpt = models.BooleanField('自动保存摘要',default=True)
    created_time = models.DateTimeField('创建时间', default=timezone.now)
    modified_time = models.DateTimeField('修改时间')
    # 摘要，可能有可能没有
    excerpt = models.CharField('摘要', max_length=200, blank=True)
    # 一对多和多对多的关系，一对多使用一个'分类'id，多对多创建一个新的表用于存放对应关系
    # (1) 分类链接分类表，外键一对多，被链接的表为那个1,on_delete代表当关联的分类(数据)被删除时，被关联的数据如何处理
    # models.CASCADE 这里指定当分类删除时，对应的文章也删除
    category = models.ForeignKey(Category, verbose_name='分类', on_delete=models.CASCADE)
    # (2) 多对多的关系，但文章可以没有标签
    tags = models.ManyToManyField(Tag, verbose_name='标签', blank=True)
    # (3) django.contrib.auth是 Django 内置的应用，专门用于网站的登录，注册，一个作者可以有多个文章，所以用外键
    # 当作者删除时，文章也删除
    author = models.ForeignKey(User, verbose_name='用户', on_delete=models.CASCADE)
    def save(self, *args, **kwargs):
        self.modified_time = timezone.now()
        if self.auto_excerpt:
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite'
            ])
            self.excerpt = strip_tags(md.convert(self.body))[:54]
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk':self.pk})

    def __str__(self):
       return self.title

