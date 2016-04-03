from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	url(r'^sales/$', 'sales.views.sales', name='sales'),
	url(r'^sales_detail/$', 'sales.views.sales_detail', name='sales_detail'),
	url(r'^sale_detail/(?P<pk>\d+)/$','sales.views.sale_detail', name='sale_detail'),
	)