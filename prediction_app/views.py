# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import ActiveMatches, Question, Choice, Participants, Activity
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from .forms import SignUpForm
from global_login_required import login_not_required
from django.template.loader import get_template
from .utils.email_utils import send_email
from django.db.models import Sum
from django.core.exceptions import PermissionDenied


LOOKUP = {
    "ActiveMatches": ActiveMatches,
    "Question": Question,
    "Choice": Choice,
    "Participants": Participants,

}


def logout_view(request):
    logout(request)
    return HttpResponse("Logged Out")


def get_model_data(request):
        # Debugging api
    model_name = request.GET.get("model_name")
    all_matches = getattr(getattr(LOOKUP[model_name], "objects"), "all")()
    return HttpResponse(all_matches)


def index(request):
    all_matches = ActiveMatches.objects.all()
    return render(request, 'prediction_app/index.html',
                  {'all_matches': all_matches})


def match_detail(request, match_id):
    match = ActiveMatches.objects.get(pk=match_id)
    return render(request, 'prediction_app/match.html', {'match': match})



def question_detail(request, question_id):
    question = Question.objects.get(pk=question_id)
    if not allow_user(request.user, question):
        raise PermissionDenied("Operation now allowed")
    return render(request, 'prediction_app/choose_answer.html',
                  {'question': question})


def user_info(request):
    print 'USER INFO', request.user.id, request.user.username
    return HttpResponse("user info")

def allow_user(user, question):
    participated = Participants.objects.filter(user_field=user).filter(question=question)
    # return True # For debugging.
    return False if participated else True


def answer(request, question_id):
    question = Question.objects.get(pk=question_id)
    if not allow_user(request.user, question):
        raise PermissionDenied("Operation now allowed")
    try:
        user_choices = request.POST.getlist('choice', None)
        allowed_choices = Question.get_allowed_choice_count(question.question_type)
        if len(user_choices) != allowed_choices:
            return HttpResponse("Please select %s options" % allowed_choices)
        selected_choice = question.choice_set.filter(
            pk__in=user_choices)
        # Change to c.id to store id of choices instead
        selected_choice = ",".join([str(c.choice_text)
                                    for c in selected_choice])

    except (KeyError, Choice.DoesNotExist):
        raise
    Participants.objects.create(
        user_field=request.user,
        question=question,
        chosen_ans=selected_choice)
    return HttpResponse("Answer submitted successfully")


@login_not_required
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/predict')
    else:
        form = UserCreationForm()
    return render(request, 'prediction_app/signup.html', {'form': form})



def send(request):
    email = request.POST.get('mail')
    reward = request.GET.get("reward")
    email = email.split(',')
    subject = 'Invitation to ZPL'
    link = 'https://zomato.com'
    template = get_template('share_email.txt')
    context = {
      'link': link,
      'sender': request.user.username,
      'reward' : reward
    }
    message = template.render(context)
    return HttpResponse("Mail sent %s"% send_email(subject, message, email))


def activity(request):
    all_activity = Activity.objects.filter(user_field=request.user)
    total_reward = all_activity.aggregate(Sum('reward'))
    return render(request, 'prediction_app/activity.html',
                  {'all_activity': all_activity, 'total_reward': total_reward['reward__sum']})

def leaderboard(request):
    leaderboard = Activity.objects.values('user_field__username').annotate(user_reward=Sum('reward')).order_by('-user_reward')
    # leaderboard = User.objects.annotate(total_reward=Sum('activity__reward'))[0].reward
    return render(request, 'prediction_app/leaderboard.html',
                  {'leaderboard': leaderboard})

