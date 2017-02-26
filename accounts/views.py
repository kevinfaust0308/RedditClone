from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


# Create your views here.
def signup(request):
    message = ''

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:

            try:
                # try checking if user with that username already exists
                User.objects.get(username=username)
                message = 'username taken'
            except User.DoesNotExist:
                user = User.objects.create_user(username=username,
                                                password=password)
                login(request, user)
                message = "account created successfully"

        else:
            message = "passwords do not match"

    return render(request, 'accounts/signup.html', {'message': message})


def loginpage(request):
    message = ''

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)

            if 'next' in request.POST:
                return redirect(request.POST['next'])
            else:
                return redirect('/')

        else:
            message = 'unable to log you in'

    return render(request, 'accounts/login.html', {'message': message})


def logoutpage(request):
    if request.method == 'POST':
        logout(request)
        return redirect('/')
