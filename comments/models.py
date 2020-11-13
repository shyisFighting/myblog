from django.db import models
from django.utils import timezone

class Comment(models.Model):
    name = models.CharField('名字',max_length=50)
    email = models.EmailField('邮箱')
    url = models.URLField('网址',blank=True)
    text = models.TextField('内容')
    created_time = models.DateTimeField('创建时间',default=timezone.now)
    post = models.ForeignKey('blog.Post',on_delete=models.CASCADE)   # 这里又直接使用了blog.Post的奇怪用法.....

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name
        ordering = ['created_time']
    def __str__(self):
        return '{}.{}'.format(self.name,self.text[:20])


