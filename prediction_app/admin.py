# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from . import models


class QuestionAdmin(admin.ModelAdmin):
    readonly_fields = ('correct_ans',)

admin.site.register(models.Question, QuestionAdmin)

class ActiveMatchesAdmin(admin.ModelAdmin):
    readonly_fields = ('match_id',
        # 'match_completed' # Remove this comment
        )

admin.site.register(models.ActiveMatches, ActiveMatchesAdmin)


# class ChoiceAdmin(admin.ModelAdmin):
#     readonly_fields = ('correct_ans',)

# admin.site.register(models.Choice, ChoiceAdmin)

# class ParticipantsAdmin(admin.ModelAdmin):
#     readonly_fields = ('correct_ans',)

# admin.site.register(models.Participants, ParticipantsAdmin)



# Register your models here.

# admin.site.register(models.ActiveMatches)

admin.site.register(models.Choice)
admin.site.register(models.Participants) # Comment this line out
admin.site.register(models.Eligibility)
admin.site.register(models.Activity)