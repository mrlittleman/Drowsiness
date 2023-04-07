from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
# Create your views here.



def login_view(request):
    template = 'landing.html'
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            print('Wrong Credentials')
            return redirect(template)
    return render(request, template)


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def Dashboard(request):
    template = 'index.html'
    return render(request, template)