from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$','accounts.views.signin'),
    url(r'^signup/$','accounts.views.signup'),
    url(r'^auth/$','accounts.views.auth_view'),
    url(r'^signout/$','accounts.views.signout'),
    url(r'^dashboard/$','accounts.views.dashboard'),
    url(r'^invalid/$','accounts.views.invalid'),
    url(r'^registered/$', 'accounts.views.register_success'),
    url(r'^not_active/$','accounts.views.not_active'),
    url(r'^confirm/(?P<activation_key>\w+)/', 'accounts.views.register_confirm'),
    url(r'^change_password/$', 'django.contrib.auth.views.password_change', name='change_password'),
    url(r'^change_password/done/$', 'django.contrib.auth.views.password_change_done', name='password_change_done'),
    url(r'^password_reset/$', 'django.contrib.auth.views.password_reset', name='password_reset'),
    url(r'^password_reset/done/$', 'django.contrib.auth.views.password_reset_done', name='password_reset_done'),
    url(r'^(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', name='password_reset_confirm'),
    url(r'^reset_done/$', 'django.contrib.auth.views.password_reset_complete', name='password_reset_complete'),
)
