# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class Option(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    is_active = models.BooleanField(default=False)
    price = models.IntegerField()

    def __unicode__(self):
        return self.name


class Registration(models.Model):
    user = models.ForeignKey(User)
    merchant_uid = models.CharField(max_length=32)
    option = models.ForeignKey(Option, null=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    company = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=20)
    transaction_code = models.CharField(max_length=36)
    payment_method = models.CharField(
        max_length=20,
        default='card',
        choices=(
            ('card', u'신용카드'),
        )
    )
    payment_status = models.CharField(max_length=10)
    payment_message = models.CharField(max_length=255, null=True)
    vbank_num = models.CharField(max_length=255, null=True, blank=True)
    vbank_name = models.CharField(max_length=20, null=True, blank=True)
    vbank_date = models.CharField(max_length=50, null=True, blank=True)
    vbank_holder = models.CharField(max_length=20, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
