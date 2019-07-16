# -*- coding: utf-8 -*-
from __future__ import unicode_literals


# Create your models here.

from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model


class ActiveMatches(models.Model):
    match_text = models.CharField(max_length=50, default='SOME STRING')

    def __str__(self):
        return self.match_text


class Question(models.Model):
    match = models.ForeignKey(ActiveMatches)
    question_text = models.CharField(max_length=200)
    correct_ans = models.CharField(max_length=20, default="None")

    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question)
    choice_text = models.CharField(max_length=200)

    def __str__(self):
        return self.choice_text

class Participants(models.Model):
    user_field = models.ForeignKey(get_user_model(), default=0)
    question = models.ForeignKey(Question)
    chosen_ans = models.CharField(max_length=200, default="None")

    def __str__(self):
        return "::".join((map(str,[self.user_field, self.question, self.chosen_ans])))

class Reward(models.Model):
    user_field = models.ForeignKey(get_user_model(), default=0)
    reward = models.IntegerField()

    def __str__(self):
        return self.reward


