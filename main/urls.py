
from django.urls import path, include
from django.views.generic.base import TemplateView
from . import views

urlpatterns = [
  
    path('accounts/', include('django.contrib.auth.urls')),
    path('' , views.home , name="home"),
    path('register', views.register_request, name="register"),
    path('news', views.news, name='news'),
    path('add-blog', views.add_blog, name='add_blog'),
    path('see-blog' , views.see_blog , name="see_blog"),
    path('blog-detail/<slug>' , views.blog_detail , name="blog_detail"),
    path('blog-delete/<id>' , views.blog_delete , name="blog_delete"),
    path('blog-update/<slug>/' , views.blog_update , name="blog_update"),
]