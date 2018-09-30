from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

# Create your views here.


def signup(req):
    if req.method == 'POST':
        if req.POST['password1'] == req.POST['password2']:
            try:
                user = User.objects.get(username=req.POST['username'])
                return render(req, 'accounts/signup.html', {'error': 'Username is already taken!'})
            except User.DoesNotExist:
                user = User.objects.create_user(
                    req.POST['username'], password=req.POST['password1'])
                login(req, user)
                return render(req, 'accounts/signup.html')
        else:
            return render(req, 'accounts/signup.html', {'error': 'Passwords are not matching!'})
    else:
        return render(req, 'accounts/signup.html')


def loginUser(req):
    if req.method == 'POST':
        user = authenticate(
            req, username=req.POST['username'], password=req.POST['password'])
        if user is not None:
            login(req, user)
            if 'next' in req.POST:
                return redirect(req.POST['next'])
            return render(req, 'accounts/login.html', {'error': 'Logged in successfully! ' + req.POST['username']})
        else:
            return render(req, 'accounts/login.html', {'error': 'Username or password is incorrect!'})
    else:
        return render(req, 'accounts/login.html')
