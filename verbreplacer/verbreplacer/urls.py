from django.conf.urls import include, url
from django.contrib import admin
from replacer.views import index

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', index),
    url(r'^query/', include('replacer.urls'))
]
