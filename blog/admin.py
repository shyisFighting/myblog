from django.contrib import admin
from .models import Tag, Category, Post

class PostAdmin(admin.ModelAdmin):

    # 表单所展示的
    list_display = ['title', 'category', 'created_time', 'modified_time', 'author']
    # 创建时所展示的，这里其实还有方法可以细分
    fields = ['title', 'body', 'excerpt', 'auto_excerpt', 'category', 'tags']
    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Post, PostAdmin)
