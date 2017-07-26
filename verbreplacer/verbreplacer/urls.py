from django.conf.urls import include, url
from django.contrib import admin
from replacer.views import index, sent_input

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', index),
    url(r'^query/(?P<sent>[\w\s]*)', sent_input)
    # url(r'^query/', include('replacer.urls')),
    # url(r'^_query/(?P<sent>[\w\s]+)', _sent_input)
]
