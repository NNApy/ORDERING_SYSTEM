from django.conf.urls import url, include
from django.contrib import admin

from ordering_app.views import add_order, orders, edit, delete, create_admin

urlpatterns = [
    url(r'^create_admin', create_admin, name='create_admin'),
    url(r'^delete', delete, name='del'),
    url(r'^edit', edit, name='edit'),
    url(r'^orders/', orders),
    url(r'^$', add_order, name='add_order'),
    url(r'^accounts/', include('django.contrib.auth.urls')),
]
