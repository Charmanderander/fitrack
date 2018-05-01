"""vjj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from . import views

urlpatterns = [
    path(r'', views.index),
    path('season1', views.s1),
    path('season2', views.s2),
    path('season3', views.s3),
    path('allseasons', views.alls),
    path('about', views.about),
    path('suggest', views.suggest),
    path('login', views.login),
    path('contestant1', views.c1),
    path('contestant2', views.c2),
    path('updateSession', views.updateSession),
    path('admin/', admin.site.urls),
]
