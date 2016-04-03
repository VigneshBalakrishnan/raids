from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'helpdesk.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'',include('accounts.urls')),
    url(r'^', include('userdetails.urls')),
    url(r'^', include('xhelp.urls')),
	url(r'^', include('contactus.urls')),
	url(r'^', include('sales.urls')),

)
