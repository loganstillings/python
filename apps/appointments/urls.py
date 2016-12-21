from django.conf.urls import url
from .import views
urlpatterns = [
    url(r'^appointments$', views.index),
    url(r'^add$', views.add),
    url(r'^edit/(?P<appointment_id>\d*)$', views.edit),
    url(r'^update/(?P<appointment_id>\d*)$', views.update),
    url(r'^delete/(?P<appointment_id>\d*)$', views.delete),
]
