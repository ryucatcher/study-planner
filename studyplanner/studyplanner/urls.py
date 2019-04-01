"""studyplanner URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls import url

from app import views
from app import api

urlpatterns = [
    # View urls
    path('admin/', admin.site.urls),
    path('index/', views.index),
    path('', views.login),
    path('login/', views.login),
    path('createaccount/', views.createAccount),
    path('dashboard/', views.dashboard),
    path('deadlines/',views.deadlines),
    url(r'^assessment/(?P<id>[-@\w]+)/$', views.assessment,name='assessment'),
    url(r'^task/(?P<id>[-@\w]+)/$', views.task,name='task'),
    url(r'^activity/(?P<id>[-@\w]+)/$', views.activity,name='activity'),

    # Forms
    path('processlogin/', views.processLogin),
    path('processaccount/', views.processAccount),
    path('logout/', views.logout),
    path('uploadhubfile/', views.uploadHubFile),

    # API urls
    path('api/updatedeadlinename', api.updateDeadlineName),
    path('api/updatetaskprogress', api.updateTaskProgress),
    path('api/getstudyprofile', api.getUserStudyProfile)
]
