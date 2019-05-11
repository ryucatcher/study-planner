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
    url(r'^milestone/(?P<id>[-@\w]+)/$', views.milestone,name='milestone'),
    path('modules/', views.module),
    path('modules/moduleInformation/', views.moduleInformation),

    # Forms
    path('processlogin/', views.processLogin),
    path('processaccount/', views.processAccount),
    path('logout/', views.logout),
    path('uploadhubfile/', views.uploadHubFile),

    # API urls
    path('api/updatedeadlinename', api.updateDeadlineName),
    path('api/updatetaskprogress', api.updateTaskProgress),
    path('api/getstudyprofile', api.getUserStudyProfile),
    path('api/changesemester', api.changeSemester),
    url(r'^assessment/(?P<id>[-@\w]+)/editname/$', api.edit_assessment_name,name='edit_assessment_name'),
    url(r'^assessment/(?P<id>[-@\w]+)/editdescription/$', api.edit_assessment_description,name='edit_assessment_description'),
    url(r'^assessment/(?P<id>[-@\w]+)/editstartdate/$', api.edit_assessment_startdate,name='edit_assessment_startdate'),
    url(r'^assessment/(?P<id>[-@\w]+)/editdeadline/$', api.edit_assessment_deadline,name='edit_assessment_deadline'),
    url(r'^assessment/(?P<id>[-@\w]+)/addmilestone/$', api.add_milestone,name='add_milestone'),
    url(r'^task/(?P<id>[-@\w]+)/editname/$', api.edit_task_name,name='edit_task_name'),
    url(r'^task/(?P<id>[-@\w]+)/editdescription/$', api.edit_task_description,name='edit_task_description'),
    url(r'^task/(?P<id>[-@\w]+)/editduration/$', api.edit_task_duration,name='edit_task_duration'),
    url(r'^task/(?P<id>[-@\w]+)/deletereqtask/$', api.delete_req_task,name='delete_req_task'),
    url(r'^task/(?P<id>[-@\w]+)/addreqtask/$', api.add_req_task,name='add_req_task'),
    url(r'^task/(?P<id>[-@\w]+)/addactivity/$', api.add_activity,name='add_activity'),
    url(r'^task/(?P<id>[-@\w]+)/addnote/$', api.add_note,name='add_note'),
    url(r'^task/(?P<id>[-@\w]+)/deletenote/$', api.delete_note,name='delete_note'),
    url(r'^task/(?P<id>[-@\w]+)/delete/$', api.delete_task,name='delete_task'),
    url(r'^activity/(?P<id>[-@\w]+)/editname/$', api.edit_act_name,name='edit_act_name'),
    url(r'^activity/(?P<id>[-@\w]+)/editcompleted/$', api.edit_act_completed,name='edit_act_completed'),
    url(r'^activity/(?P<id>[-@\w]+)/edittarget/$', api.edit_act_target,name='edit_act_target'),
    url(r'^activity/(?P<id>[-@\w]+)/addnote/$', api.add_note_act,name='add_note_act'),
    url(r'^activity/(?P<id>[-@\w]+)/deletenote/$', api.delete_note_act,name='delete_note_act'),
    url(r'^activity/(?P<id>[-@\w]+)/addtask/$', api.add_task_to_act,name='add_task_to_act'),
    url(r'^activity/(?P<id>[-@\w]+)/deletetask/$', api.delete_task_from_act,name='delete_task_from_act'),
    url(r'^activity/(?P<id>[-@\w]+)/delete/$', api.delete_act,name='delete_act'),
    url(r'^milestone/(?P<id>[-@\w]+)/editname/$', api.edit_ms_name,name='edit_ms_name'),
    url(r'^milestone/(?P<id>[-@\w]+)/deletereqtask/$', api.delete_ms_req_task,name='delete_ms_req_task'),
    url(r'^milestone/(?P<id>[-@\w]+)/addreqtask/$', api.add_ms_req_task,name='add_ms_req_task'),
    url(r'^milestone/(?P<id>[-@\w]+)/delete/$', api.delete_ms,name='delete_ms')
]
