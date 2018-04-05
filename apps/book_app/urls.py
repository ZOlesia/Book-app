from django.conf.urls import url
from . import views           # This line is new!
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^books$', views.home),
    url(r'^books/add$', views.add),
    url(r'^books/create$', views.create),
    url(r'^books/proccess/(?P<id>\d+)$', views.proccess),
    url(r'^books/(?P<id>\d+)$', views.book),
    url(r'^users/(?P<id>\d+)$', views.user),
]

