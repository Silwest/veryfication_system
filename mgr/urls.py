from django.conf.urls import patterns, include, url
from mgr import views

urlpatterns = patterns(
    '',
    url(r'^$', views.main_page, name='main_page'),
    url(r'^allquestions$', views.all_questions, name='all_questions'),
    url(r'^createtest', views.create_test, name='create_test'),
    url(r'^choosedepartment$', views.choose_department, name='choose_department'),
    url(r'^showfieldofquestion/(\d+)$', views.show_field_of_question, name='show_field_of_questions'),
    url(r'^workonquestion/?$', views.work_on_question, name='work_on_questions'),
    url(r'^savequestion/(?P<question_id>(\d+))/(?P<accept>(\w+))/?$', views.save_question, name='save_question'),
    url(r'^acceptquestion/?$', views.accept_question, name='accept_question'),
    url(r'^loadquestions/(?P<field_of_question_id>(\d+))/?$', views.load_questions_field_of_question, name='load_questions'),
    url(r'^starttest/(?P<field_of_question>(\w+))/?', views.start_test, name='start_test'),
    url(r'^checkanswers/?', views.check_answers, name='check_answers'),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'registration/login.html'}),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
)
