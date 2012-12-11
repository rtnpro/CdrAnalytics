from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'CdrAnalytics.cdr.views.home', name='home'),
    url(
        r'^analytics/max_con_call_count/$',
        'CdrAnalytics.cdr.views.max_con_call_analytics',
        name='max_con_call_analytics'
    ),
    url(
        r'^analytics/pi_call_stats/$',
        'CdrAnalytics.cdr.views.pi_call_stats_analytics',
        name='pi_call_stats_analytics'
    )
)

urlpatterns += staticfiles_urlpatterns()
