from django.conf.urls import patterns, include, url
from haystack.views import SearchView


urlpatterns = patterns('haystack.views',
    url(r'^$', SearchView(results_per_page=15), name='haystack_search'),
)
