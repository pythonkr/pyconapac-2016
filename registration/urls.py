from django.conf.urls import patterns, include, url
import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^status/$', views.status, name='registration_status'),
    url(r'^payment/$', views.payment, name='registration_payment'),
]
