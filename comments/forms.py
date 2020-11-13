from django import forms
from .models import Comment
## 表单类型类与数据模型ORM相似，会帮我们生成html表单
class CommentForm(forms.ModelForm): # 使用一个数据库模型
    class Meta:
        model = Comment  # 表单对应的模型
        fields = ['name','email','url','text']
