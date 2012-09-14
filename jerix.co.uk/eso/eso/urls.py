from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'eso.views.home', name='home'),
    # url(r'^eso/', include('eso.foo.urls')),

    url(r'^modules/(?P<module_id>\d+)/(?P<slug>.+)/posts/$', 'modules.views.module_posts', name="module-posts"),
    url(r'^modules/(?P<module_id>\d+)/posts/$', 'modules.views.module_posts'),

    (r'^questions/', include('q_and_a.urls')),

    (r'^search/', include('haystack.urls')),

    # Downloads
    (r'^download/', include('download.urls')),

    # Hitcount ajax url
    url(r'^analytics/', include('hitcount.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
   )
