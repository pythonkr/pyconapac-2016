from django.conf.urls import patterns, include, url
from django.contrib.auth.decorators import login_required

import views

urlpatterns = [
    url(r'^$', views.index, name='registration_index'),
    url(r'^status/$', views.status, name='registration_status'),
    url(r'^payment/(\d*)/$', views.payment, name='registration_payment'),
    url(r'^payment/$', views.payment_process, name='registration_payment'),
    url(r'^receipt/$',
        login_required(views.RegistrationReceiptDetail.as_view()), name='registration_receipt'),
]
