#-*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.admin.options import TabularInline, ModelAdmin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.db import models
from django.utils.translation import ugettext_lazy as _
from shop_productvariations.models import Option, OptionGroup, TextOption


class OptionInline(TabularInline):
    model = Option

class OptionGroupAdmin(ModelAdmin):
    inlines = [OptionInline,]
    prepopulated_fields = {"slug": ("name",)}
    formfield_overrides = {
        models.ManyToManyField: {'widget': FilteredSelectMultiple(
            verbose_name=_('grouped options'),
            is_stacked=False
            )},
    }

admin.site.register(OptionGroup, OptionGroupAdmin)


class TextOptionAdmin(ModelAdmin):
    formfield_overrides = {
        models.ManyToManyField: {'widget': FilteredSelectMultiple(
            verbose_name=_('text options'),
            is_stacked=False
            )},
    }

admin.site.register(TextOption, TextOptionAdmin)
