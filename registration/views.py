# -*- coding: utf-8 -*-
import logging
import datetime
from uuid import uuid4

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.utils.translation import ugettext as _
from django.conf import settings
from django.contrib.auth.decorators import login_required
from constance import config

from pyconkr.helper import send_email_ticket_confirm, render_io_error
from .forms import RegistrationForm
from .models import Option, Registration
from iamporter import get_access_token, Iamporter, IamporterError

logger = logging.getLogger(__name__)
payment_logger = logging.getLogger('payment')

_is_ticket_open = lambda : True if config.REGISTRATION_OPEN <= datetime.date.today() <= config.REGISTRATION_CLOSE else False

def index(request):
    if request.user.is_authenticated():
        is_registered = Registration.objects.filter(
            user=request.user,
            payment_status__in=['paid', 'ready']
        ).exists()
    else:
        is_registered = False
    options = Option.objects.filter(is_active=True)
    return render(request, 'registration/info.html',
                  {'is_ticket_open': _is_ticket_open,
                   'options': options,
                   'is_registered': is_registered})

@login_required
def status(request):
    registration = Registration.objects.get(user=request.user)
    return render(request, 'registration/status.html', {'registration': registration})

@login_required
def payment(request, option_id=None):
    form = RegistrationForm()

    if not _is_ticket_open():
        return redirect('registration_info')

    product = Option.objects.get(id=option_id)

    registered = Registration.objects.filter(
        user=request.user,
        payment_status__in=['paid', 'ready']
    ).exists()

    if registered:
        return redirect('registration_status')

    uid = str(uuid4()).replace('-', '')
    form = RegistrationForm(initial={'email': request.user.email,
                                     'option': product})

    return render(request, 'registration/payment.html', {
        'title': _('Registration'),
        'form': form,
        'uid': uid,
        'product_name': product.name,
        'amount': product.price,
        'vat': 0,
    })

def payment_process(request):
    if request.method == 'GET':
        return redirect('registration_index')

    payment_logger.debug(request.POST)
    form = RegistrationForm(request.POST)

    # TODO : more form validation
    # eg) merchant_uid
    if not form.is_valid():
        form_errors_string = "\n".join(('%s:%s' % (k, v[0]) for k, v in form.errors.items()))
        return JsonResponse({
            'success': False,
            'message': form_errors_string,  # TODO : ...
        })

    remain_ticket_count = (config.TOTAL_TICKET - Registration.objects.filter(payment_status__in=['paid', 'ready']).count())

    # sold out
    if remain_ticket_count <= 0:
        return JsonResponse({
            'success': False,
            'message': u'티켓이 매진 되었습니다',
        })

    registration, _ = Registration.objects.get_or_create(user=request.user)
    registration.name = form.cleaned_data.get('name')
    registration.email = request.user.email
    registration.company = form.cleaned_data.get('company', '')
    registration.phone_number = form.cleaned_data.get('phone_number', '')
    registration.merchant_uid = request.POST.get('merchant_uid')
    registration.option = form.cleaned_data.get('option')
    registration.save()  # TODO : use form.save()

    try:
        product = registration.option
        access_token = get_access_token(config.IMP_API_KEY, config.IMP_API_SECRET)
        imp_client = Iamporter(access_token)

        if request.POST.get('payment_method') == 'card':
            # TODO : use validated and cleaned data
            imp_client.onetime(
                token=request.POST.get('token'),
                merchant_uid=request.POST.get('merchant_uid'),
                amount=product.price,
                # vat=request.POST.get('vat'),
                card_number=request.POST.get('card_number'),
                expiry=request.POST.get('expiry'),
                birth=request.POST.get('birth'),
                pwd_2digit=request.POST.get('pwd_2digit'),
                customer_uid=form.cleaned_data.get('email'),
            )

        confirm = imp_client.find_by_merchant_uid(request.POST.get('merchant_uid'))

        if confirm['amount'] != product.price:
            # TODO : cancel
            return render_io_error("amount is not same as product.price. it will be canceled")

        registration.payment_method = confirm.get('pay_method')
        registration.payment_status = confirm.get('status')
        registration.payment_message = confirm.get('fail_reason')
        registration.vbank_name = confirm.get('vbank_name', None)
        registration.vbank_num = confirm.get('vbank_num', None)
        registration.vbank_date = confirm.get('vbank_date', None)
        registration.vbank_holder = confirm.get('vbank_holder', None)
        registration.save()

        if not settings.DEBUG:
            send_email_ticket_confirm(request, registration)
    except IamporterError as e:
        # TODO : other status code
        return JsonResponse({
            'success': False,
            'code': e.code,
            'message': e.message,
        })
    else:
        return JsonResponse({
            'success': True,
        })
