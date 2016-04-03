from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'helpdesk.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^add_help/$', 'xhelp.views.add_help', name='add_help'),
    url(r'^help/list/$', 'xhelp.views.help_list', name='help_list'),
    url(r'^help_detail/(?P<pk>\d+)/$','xhelp.views.help_detail', name='help_detail'),
    )