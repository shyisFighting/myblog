from django.urls import path
from . import views
app_name = 'blog'  # 这样我们就可以通过app_name 在其他文件得到到这个url，传入参数
# 将网址和处理函数的关系写在urlpatterns列表里
# path第一个参数为网址，第二个为处理函数，第三个为处理函数别名
urlpatterns = [
    path('', views.index, name='index'),
    path('post/<int:pk>/', views.detail, name='detail'),
    path('archives/<int:year>/<int:month>/',views.archive,name='archive'), #排版布局仍然使用index
    path('categories/<int:pk>',views.category,name='category'),
]