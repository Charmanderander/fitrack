"""nineku URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()
from nineku import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^register', views.register_user),
    url(r'^success', views.register_success),
    url(r'^already_confirmed', views.already_confirmed),
    url(r'^post', views.upload),
    url(r'^login', views.login),
    url(r'^logout', views.logout),
    url(r'^myPosts', views.viewUserPosts),
    url(r'^search', views.search),
    url(r'^confirm/(?P<activation_key>\w+)/', views.register_confirm),
    url(r'^$', views.main),
]
