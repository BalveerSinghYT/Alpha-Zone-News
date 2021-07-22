
from django.urls import path, include
from django.views.generic.base import TemplateView
from . import views
urlpatterns = [
  
    path('accounts/', include('django.contrib.auth.urls')),
    path('', TemplateView.as_view(template_name = 'home.html'), name = 'home'),
    path('register', views.register_request, name="register"),

]