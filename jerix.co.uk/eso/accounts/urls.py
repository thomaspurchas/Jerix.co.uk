from django.conf.urls import patterns, include, url

urlpatterns = patterns('accounts.views',
    url(r'^login/', 'login_user', name='user-login'),

)