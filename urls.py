from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^status/$', views.status),
    url(r'^gold/$', views.gold),
    url(r'^gold/(?P<method>\w+)/$', views.gold_method),
]
