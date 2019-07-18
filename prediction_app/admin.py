# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.ActiveMatches)
admin.site.register(models.Question)
admin.site.register(models.Choice)
admin.site.register(models.Participants)
admin.site.register(models.Eligibility)
admin.site.register(models.Activity)