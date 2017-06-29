from django.conf.urls import url

# from . import views
from replacer.views import sent_input


urlpatterns = [
    # url(r'^$', views.index, name='index'),
    url(r'^$', sent_input)
]