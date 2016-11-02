"""facebook_post_service URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from post import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.query, name='query'),
    url(r'^post/(?P<query>.+)/(?P<mode>[_]?)$', views.post, name='post'),
    url(r'^post/(?P<status_id>\d+_\d+)/edit$', views.post_edit, name='post_edit'),
    url(r'^comment$', views.comment, name='comment'),
    url(r'^retrieve_post$', views.retrieve_post, name='retrieve_post'),

    url(r'^login', views.user_login, name='user_login'),
    url(r'^signup', views.user_signup, name='user_signup'),
    url(r'^logout', views.user_logout, name='user_logout'),
]
