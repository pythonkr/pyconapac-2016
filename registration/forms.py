# -*- coding: utf-8 -*-
from django import forms
from .models import Registration
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Div


class RegistrationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):

        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['readonly'] = True
        self.fields['option'].widget.attrs['disabled'] = True
        self.helper = FormHelper()
        self.helper.form_id = 'registration-form'
        self.helper.form_method = 'post'
        self.helper.add_input(Div('additional_price', id='additional_price'))
        self.helper.add_input(Submit('submit', u'결제하기', disabled='disabled'))

    class Meta:
        model = Registration
        fields = ('email', 'option', 'name', 'company', 'phone_number', 'payment_method')
        labels = {
            'name': u'이름',
            'option': u'옵션',
            'email': u'이메일',
            'company': u'소속',
            'phone_number':  u'전화번호',
            'payment_method': u'결제수단',
        }
