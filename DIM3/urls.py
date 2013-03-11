from django.conf.urls import patterns, include, url

from cocoandco import views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'DIM3.views.home', name='home'),
    # url(r'^DIM3/', include('DIM3.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
     url(r'^createpost/$', views.createpost, name='createpost'),
     url(r'^post/(?P<post_id_url>\d+)/$', views.post, name='post'),
     url(r'^$', views.index, name='index'),
     url(r'^login/$', views.login, name='login'),
     url(r'^cat/(?P<category_name>\w+)', views.category, name='category'),
     url(r'^register/$', views.register, name='register'),
     url(r'^user/(?P<user_id_url>\d+)/$', views.user, name='user'),
     
)
