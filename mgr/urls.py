from django.conf.urls import patterns, include, url
from mgr import views

urlpatterns = patterns(
    '',
    url(r'^$', views.main_page, name='main_page'),
    url(r'^allquestions$', views.all_questions, name='all_questions'),
    url(r'^choosedepartment$', views.choose_department, name='choose_department'),
    url(r'^showfieldofquestions/(\d+)$', views.show_field_of_questions, name='show_field_of_questions'),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'registration/login.html'}),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
)