# -*- coding: utf-8 -*-
from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import Registration, Option


class OptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'price')
    list_editable = ('is_active',)
    ordering = ('id',)
admin.site.register(Option, OptionAdmin)


class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('user', 'option', 'name', 'email')
    ordering = ('id',)
admin.site.register(Registration, RegistrationAdmin)
