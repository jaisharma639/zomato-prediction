# -*- coding: utf-8 -*-
from __future__ import unicode_literals


# Create your models here.

from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from jsonfield import JSONField


class ActiveMatches(models.Model):
    match_text = models.CharField(max_length=50, default='SOME STRING')
    match_id = models.PositiveSmallIntegerField(default=0)
    match_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.match_text

    @classmethod
    def get_all_mid(cls):
        all_matches = cls.objects.all()
        return {match.match_id for match in all_matches}

    @classmethod
    def get_running_matches(cls):
        return cls.objects.filter(match_completed=False)

    @classmethod
    def create_entry(cls, match_id, match_text):
        cls.objects.create(match_id=match_id, match_text=match_text)
        return

    @classmethod
    def delete_entries(cls, ids):
        cls.objects.filter(match_id__in=ids).delete()


class Question(models.Model):
    match = models.ForeignKey(ActiveMatches)
    question_text = models.CharField(max_length=200)
    correct_ans = models.CharField(max_length=20, default="None")
    question_type = models.CharField(max_length=1, default="a")

    def __str__(self):
        return "::".join((map(str, [self.match, self.question_text,
                                    self.correct_ans, self.question_type])))

    @classmethod
    def get_allowed_choice_count(cls, question_type):
        if question_type == 'a':
            return 1
        elif question_type == 'b':
            return 3


class Choice(models.Model):
    question = models.ForeignKey(Question)
    choice_text = models.CharField(max_length=200)

    def __str__(self):
        return self.choice_text


class Participants(models.Model):
    user_field = models.ForeignKey(get_user_model(), default=0)
    question = models.ForeignKey(Question)
    chosen_ans = models.CharField(max_length=200, default="None")
    reward = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return "::".join((map(str, [self.user_field, self.question,
                                    self.chosen_ans, self.reward])))

class Activity(models.Model):
    user_field = models.ForeignKey(get_user_model(), default=0)
    information = models.CharField(max_length=200, default="None")
    reward = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return "::".join((map(str, [self.user_field, self.information,
                                    self.reward])))


class Eligibility(models.Model):
    question = models.ForeignKey(Question)
    eligibility = JSONField()

    def __str__(self):
        return "::".join((map(str, [self.question, self.eligibility])))
