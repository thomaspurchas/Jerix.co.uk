from django.conf.urls import patterns, url

urlpatterns = patterns('files.views',
    url(r'^original/(?P<id>\d+)/(?P<slug>.*)$', 'original_download',
                                                     name='download-original'),
    url(r'^derived/(?P<id>\d+)/(?P<orig_id>\d+)/(?P<slug>.*)$',
                        'derived_download', name='download-derived-with-orig'),
    url(r'^derived/(?P<id>\d+)/(?P<slug>.*)$',
                                'derived_download', name='download-derived'),
    url(r'^s3/(?P<id>\d+)/(?P<slug>.*)$', 'original_download',
                                                     name='download-original'),
)
