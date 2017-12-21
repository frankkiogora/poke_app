# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from .models import User
from .models import Poke
from django.contrib import messages

#==================================================#
#                  RENDER METHODS                  #
#==================================================#

def index(request):
    context = {
        'users': User.objects.all()
    }
    return render(request, "poke_app/index.html", context)


def pokes(request):
    try:

        logged_user = User.objects.get(id=request.session['user_id'])
    except KeyError:
        return redirect('/')
    context = {
        'user': User.objects.get(id=request.session['user_id']),
        'poker': Poke.objects.all(),
        'poke_count': Poke.objects.filter(poked_by = logged_user),
        'poke_total': Poke.objects.filter(poked_by = logged_user).values('poker').count(),
        'others': User.objects.exclude(id=request.session['user_id']),
    }
    return render(request, "poke_app/poke.html", context)


#==================================================#
#                 PROCESS METHODS                  #
#==================================================#

def register(request):
    result = User.objects.register_validate(request.POST)
    if type(result) == list:
        for error in result:
            messages.error(request, error)
        return redirect('/')

    request.session['user_id'] = result.id
    messages.success(request, "Successfully registered!")
    return redirect('/pokes')


def login(request):
    result = User.objects.login_validate(request.POST)
    if type(result) == list:
        for error in result:
            messages.error(request, error)

        return redirect ("/")

    request.session['user_id'] = result.id
    messages.success(request, "Successfully logged in!")
    return redirect("/pokes")

def logout(request):
    request.session.clear()
    return redirect ('/')

def poke_process(request):
    poker_id = User.objects.get(id=request.POST['poker_id'])
    poked_by_id = User.objects.get(id=request.POST['poked_by_id'])
    poke_process = Poke.objects.create(poker = poker_id, poked_by = poked_by_id)

    return redirect('/pokes')
