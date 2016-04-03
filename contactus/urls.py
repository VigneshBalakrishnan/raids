from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    
    url(r'^contact/$', 'contactus.views.contactus', name='contactus'),
    url(r'^invite/$', 'contactus.views.invite', name='invite'),
    url(r'^connect/(?P<pk>\d+)/$', 'contactus.views.connect', name='connect'),
    url(r'^messages/$', 'contactus.views.connect_list', name='connect_list'),
    url(r'^messages/(?P<pk>\d+)/$', 'contactus.views.connect_message', name='connect_message'),
    )