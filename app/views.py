from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
# Create your views here.

def login_view(request):
    template = 'landing.html'
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            redirect('dashboard')
    return render(request, template)

def Dashboard(request):
    template = 'index.html'
    return render(request, template)