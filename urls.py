"""URLconf of panel

将以下语句加入工程的 urls.py:

import panel.urls

urlpatterns 内添加:

url(r'^accounts/', include('django.contrib.auth.urls', namespace='auth')),
url(r'^panel/', include(panel.urls, namespace='panel')),
"""

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^ss-op/$', views.ss_op, name='ss-op'),

    url(r'^logout/$', views.quit, name='logout'),
    url(r'^password_change/$', views.password_change_panel, name='password_change'),
    url(r'^password_change/done/$', views.password_change_done, name='password_change_done'),

    url(r'^users/$', views.users, name='users'),
    url(r'^status/$', views.status, name='status'),
    url(r'^gold/$', views.gold, name='gold'),
    url(r'^gold/(?P<method>\w+)/$', views.gold_method),

    url(r'^ss-op-admin/$', views.ss_op_admin, name='ss-op-admin'),
]
