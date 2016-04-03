from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	url(r'^profile/$', 'userdetails.views.user_profile', name='user_profile'),
	url(r'^profile/display/$', 'userdetails.views.profile', name='profile'),
	url(r'^profile/show/(?P<pk>\d+)/$', 'userdetails.views.profile_disp', name='profile_disp'),
	)