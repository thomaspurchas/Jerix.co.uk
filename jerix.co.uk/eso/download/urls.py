from django.conf.urls import patterns, include, url

urlpatterns = patterns('download.views',
    url(r'^original/(?P<id>\d+)/(?P<slug>.*)$', 'original_download',
                                                     name='download-original'),
    url(r'^derived/(?P<id>\d+)/(?P<orig_id>\d+)/(?P<slug>.*)$',
                        'derived_download', name='download-derived-with-orig'),
    url(r'^derived/(?P<id>\d+)/(?P<slug>.*)$',
                                'derived_download', name='download-derived'),

)