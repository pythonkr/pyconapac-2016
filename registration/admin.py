# -*- coding: utf-8 -*-
from django.contrib import admin
from django.core.mail import send_mail, send_mass_mail
from modeltranslation.admin import TranslationAdmin

from .models import Registration, Option

def send_bankpayment_alert_email(modeladmin, request, queryset):
    messages = []
    subject = u"PyCon APAC 2016 입금확인부탁드립니다. Please Check PyCon APAC 2016 payment"
    body = u"""
    안녕하세요. PyCon APAC 준비위원회입니다.
    현재 입금여부를 확인하였으나 입금이 되지 않았습니다.
    혹시나 다른 이름으로 입금하신분은 support@pycon.kr 로 메일 부탁드립니다.
    입금시한은 구매로부터 일주일입니다.
    감사합니다.
    """
    from_email = "support@pycon.kr"
    for obj in queryset:
        email = obj.email
        message = (subject, body, from_email, [email])
    send_mass_mail(messages, fail_silently=False)

send_bankpayment_alert_email.short_description = "Send Bank Payment Email"

class OptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'price')
    list_editable = ('is_active',)
    ordering = ('id',)
admin.site.register(Option, OptionAdmin)


class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('user', 'option', 'name', 'email', 'payment_method',
                    'payment_status', 'created', 'confirmed', 'canceled')
    list_editable = ('payment_status',)
    list_filter = ('option', 'payment_method', 'payment_status')
    search_fields = ('name', )
    readonly_fields = ('created', )
    ordering = ('id',)
    actions = (send_bankpayment_alert_email,)
admin.site.register(Registration, RegistrationAdmin)
