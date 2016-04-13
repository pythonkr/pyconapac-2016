# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import Registration
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Div


class RegistrationForm(forms.ModelForm):
    base_price = forms.IntegerField(label=_('Base price'))
    def __init__(self, *args, **kwargs):

        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['readonly'] = True
        self.fields['base_price'].widget.attrs['readonly'] = True
        self.fields['option'].widget.attrs['disabled'] = True
        self.helper = FormHelper()
        self.helper.form_id = 'registration-form'
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', u'결제하기', disabled='disabled'))

    class Meta:
        model = Registration
        fields = ('email', 'option', 'base_price', 'name', 'company', 'phone_number', 'payment_method')
        labels = {
            'name': u'이름',
            'option': u'옵션',
            'email': u'이메일',
            'company': u'소속',
            'phone_number':  u'전화번호',
            'payment_method': u'결제수단',
        }


class RegistrationAdditionalPriceForm(RegistrationForm):

    class Meta:
        model = Registration
        fields = ('email', 'option', 'base_price', 'additional_price', 'name', 'company', 'phone_number', 'payment_method')
        labels = {
            'name': u'이름',
            'option': u'옵션',
            'additional_price': u'추가후원금액 KRW',
            'email': u'이메일',
            'company': u'소속',
            'phone_number':  u'전화번호',
            'payment_method': u'결제수단'
        }
