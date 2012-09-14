from django.conf.urls import patterns, include, url
from django.conf import settings

urlpatterns = patterns('q_and_a.views',
    url(r'^(?P<question_id>\d+)/(?P<slug>.+)/?$', 'question', name="question"),

    url(r'^(?P<question_id>\d+)/$', 'question'),

    url(r'^tagged/(?P<tag>.*/?)', 'tagged')
)