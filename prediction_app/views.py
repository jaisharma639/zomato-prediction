# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect

# Create your views here.

from django.http import HttpResponse
from django.template import loader

from .models import ActiveMatches, Question, Choice, Participants

from django.shortcuts import get_object_or_404, render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from .forms import SignUpForm
from django.contrib.auth import logout
from global_login_required import login_not_required



LOOKUP = {
	"ActiveMatches": ActiveMatches,
	"Question": Question,
	"Choice": Choice,
	"Participants": Participants
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
    return render(request, 'prediction_app/index.html', {'all_matches': all_matches})


def match_detail(request, match_id):
    match = ActiveMatches.objects.get(pk=match_id)
    return render(request, 'prediction_app/match.html', {'match': match})



def question_detail(request, question_id):
    question = Question.objects.get(pk=question_id)
    return render(request, 'prediction_app/choose_answer.html', {'question': question})


def user_info(request):
    print 'USER INFO'
    print request.user.id
    print request.user.username
    print request.user.reward
    return HttpResponse("user info")


def answer(request, question_id):
    question = Question.objects.get(pk=question_id)
    try:
    	# print request.POST.getlist('choice', None), request.POST
        selected_choice = question.choice_set.filter(pk__in=request.POST.getlist('choice', None))
        print [c.id for c in selected_choice], type(selected_choice)
        selected_choice = ",".join([str(c.id) for c in selected_choice])

    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        raise
    Participants.objects.create(
    	user_field = request.user,
    	question = question,
    	chosen_ans = selected_choice)
    return HttpResponse("Participants table updated")

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
    print "can't create user"
    return render(request, 'prediction_app/signup.html', {'form': form})



