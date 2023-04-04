from django.shortcuts import render

# Create your views here.
def Dashboard(request):
    template = 'index.html'
    return render(request, template)