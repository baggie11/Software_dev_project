"""
URL configuration for loginapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin # type: ignore
from django.urls import path # type: ignore
from login import views
import _mysql_connector # type: ignore

urlpatterns = [
    path('',views.home),
    path('admin/', admin.site.urls),
    path("login/",views.login),
    path("add/",views.add),
    path("mentee/",views.mentee),
    path("mentor/",views.mentor),
    path("success/",views.success),
    path("delete/",views.delete,name = "delete"),
    path("detail/",views.detail),
    path("note/",views.note),
    path("back/",views.back),
    path("schedule/",views.schedule),
    #path("edit/",views.edit),
    path("semester/",views.semester),
    #path("questionPage/",views.questionPage),
    path("deletelatest/",views.deletelatest),
    path("forgot/",views.forgot),
    path("manager/",views.manager),
    path("enter/",views.enter),
    path("viewmarks/",views.viewmarks),
    path("logout",views.logout),
    path("postquestion/",views.postquestion),
    path("createquestion/",views.createquestion),
    path("answer/",views.answer),
    path("viewans/",views.viewans),
    path("ans/",views.ans)
]
