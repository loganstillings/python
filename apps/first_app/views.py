from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, 'first_app/index.html')

def register(request):
    viewsResponse = User.objects.add_user(request.POST)
    if viewsResponse['isRegistered']:
        request.session['user_id'] = viewsResponse['user'].id
        request.session['user_fname'] = viewsResponse['user'].first_name
        return redirect('/success')
    else:
        for error in viewsResponse['errors']:
            messages.error(request, error)
        return redirect('/')
def success(request):
    if 'user_id' not in request.session:
        messages.error(self, 'Must be logged in!')
        return redirect('/')
    return render(request, 'first_app/success.html')

def login(request):
    viewsResponse = User.objects.login_user(request.POST)
    if viewsResponse['isLoggedIn']:
        request.session['user_id'] = viewsResponse['user'].id
        request.session['user_fname'] = viewsResponse['user'].first_name
        return redirect('/success')
    else:
        for error in viewsResponse['errors']:
            messages.error(request, error)
        return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')
