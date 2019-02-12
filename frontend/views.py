from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages


def dashboard(request):
    '''Dashboard'''
    context = {
        'username': request.user.username if request.user.is_authenticated else "anonymous"
    }
    return render(request, 'frontend/dashboard.html', context)


def report_edit(request, report_id):
    '''Dashboard'''
    context = {
        'report_id': report_id,
        'username': request.user.username if request.user.is_authenticated else "anonymous"
    }
    return render(request, 'frontend/report_edit.html', context)


def statistics(request):
    '''Statistics page'''
    context = {
        'username': request.user.username if request.user.is_authenticated else "anonymous"
    }
    return render(request, 'frontend/statistics.html', context)


def logout_request(request):
    '''Logout request'''
    logout(request)
    messages.info(request, "You have been logged out !")
    return redirect("dashboard")


def login_request(request):
    '''Login request'''
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                print("Success Login")
                login(request, user)
                messages.info(request, f"Welcome {username}, you have been successfully logged in!")
                return redirect('dashboard')
            else:
                print("Failed Login")
                messages.warning(request, "Invalid Username or Password !")
        else:
            messages.warning(request, "Invalid Form !")

    form = AuthenticationForm()
    return render(request, "frontend/login.html", {'form': form})
