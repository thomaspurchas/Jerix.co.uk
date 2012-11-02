from django.conf.urls import patterns, include, url

urlpatterns = patterns('accounts.views',
    url(r'^login/', 'login_user', name='login'),

)

urlpatterns += patterns('',
    url(r'^logout/', 'django.contrib.auth.views.logout', name='logout')
)