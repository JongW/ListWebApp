# http requests
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

# log in
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
# models
from .models import List
# misc
import datetime


def login_attempt(request):
    password = request.POST.get('password')
    username = request.POST.get('username')
    user = authenticate(request, username=username, password=password)

    message = ''
    if request.method == "POST":
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("home"))
        else:
            message = 'failed login'

    context = {'message': message}
    return render(request, "home/login.html", context)


def create_user(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    email = request.POST.get('email')

    if request.method == "POST":
        if User.objects.filter(username=username).exists():
            context = {'message' : 'user exists!'}
            return render(request, "home/create_user.html", context)
        else:
            User.objects.create_user(username, email, password)
            context = {'message': "welcome" + username}
            return render(request, "home/create_user.html", context)

    return render(request, "home/create_user.html")


def logout_attempt(request):
    logout(request)
    return HttpResponseRedirect(reverse("log_in"))


@login_required
def home(request):
    current_user = request.user
    if request.method == 'POST' and not request.is_ajax():
        input_box = request.POST.get('inputBox')
        if input_box is not None:
            s = List.objects.last()
            if s is not None:
                new_id = s.private_id
                List.objects.create(todo_text=input_box, pub_date=datetime.datetime.now(), complete=False,
                                    private_id=new_id + 1, user_name=current_user.username)
                return HttpResponseRedirect(reverse("home"))
            else:
                List.objects.create(todo_text=input_box, pub_date=datetime.datetime.now(), complete=False, private_id=1,
                                    user_name=current_user.username)
                return HttpResponseRedirect(reverse("home"))

    if request.is_ajax() and request.method == "POST":
        to_delete = int(request.POST.get('id'))
        last = List.objects.last().private_id
        List.objects.get(private_id=to_delete).delete()

        while to_delete < last:
            s = List.objects.get(private_id=to_delete + 1)
            s.private_id = s.private_id - 1
            s.save()
            to_delete = to_delete + 1

    return render_list(request)


def render_list(request):
    current_user = request.user
    try:
        todo_array = List.objects.filter(user_name=current_user.username)
        length = len(todo_array)
    except:
        todo_array = None
        length = 0

    context = {'todo_array': todo_array,
               'length': length}
    return render(request, 'home/mainList.html', context)
