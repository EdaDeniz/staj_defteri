"""staj_defteri URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls import url, include
from django.contrib import admin
import blog
import project
from project import views
from blog import views
from attendance import views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^post/(?P<pk>\d+)/$', blog.views.PostComment.as_view(), name='post_detail'),
    url(r'^detail/(?P<pk>\d+)/$', blog.views.all_posts_detail.as_view(), name='all_posts_detail'),
    url(r'^detail$', blog.views.all_posts_detail.as_view(), name='all_posts_detail'),
    url(r'', include('blog.urls')),
    url(r'^$', blog.views.all_posts, name='home'),
    url(r'^project/new/$', project.views.project_new, name="new_project"),
    url(r'^project/(?P<pk>\d+)/$', project.views.project_details, name='project_detail'),
    url(r'myprojects/$', project.views.all_projects, name='projects'),
    url(r'^attendance/$', views.attendanceView, name="attendance"),
    url(r'^myattendance/$', views.AttendanceCounter, name="myattendance"),
    url(r'^internship/$', views.Internship, name="internship"),

]
