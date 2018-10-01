from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from blog import views
from project.views import project_delete, project_update


urlpatterns = [
    url(r'^post$', views.PostComment.as_view(), name='post_detail'),
    url(r'^post/(?P<pk>\d+)/$', views.PostComment.as_view(), name='post_detail'),
    # url(r'^mypost$', views.PostComment.as_view(), name='mypost'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/$', auth_views.login, {'template_name': '/home/eda/staj_defteri/templates/login.html'}),
    url(r'^logout/$', auth_views.logout, {'next_page': '/login/'}, name='logout'),
    url(r'myposts/$', views.index_page, name='myposts'),
    url(r'^home/$', views.all_posts, name="all_posts"),
    url(r'^post/(?P<pk>\d+)/update/$', views.post_update, name='update'),
    url(r'^post/(?P<pk>\d+)/delete/$', views.post_delete, name='delete'),
    url('^', include('django.contrib.auth.urls')),
    url(r'^project/(?P<pk>\d+)/delete/$', project_delete, name='delete_project'),
    url(r'^project/(?P<pk>\d+)/update/$', project_update, name='update_project'),
    url(r'^recommendations/$', views.recommendations, name='recommendations'),
]
