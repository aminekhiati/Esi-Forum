from django.shortcuts import render, redirect

from .forms import SignUpForm
from django.http import HttpResponse
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm




def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            utilisateur = form.save()
            utilisateur.refresh_from_db()  # load the profile instance created by the signal
            if(form.cleaned_data.get('phone_number')):
                utilisateur.profile.numero_telephone = form.cleaned_data.get('phone_number')
            if(form.cleaned_data.get('promo')):
                utilisateur.profile.promotion = form.cleaned_data.get('promo')
            if(form.cleaned_data.get('bio')):
                utilisateur.profile.bio = form.cleaned_data.get('bio')
            utilisateur.save()
            return HttpResponse('success')
    else:
        form = SignUpForm()
    return render(request, 'Main/registration.html', {'form': form})


def logout_request(request):
    logout(request)
    messages.info(request,"Logged out successfully")
    return redirect("")

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Logged in successfully as {username}")
                return redirect('../home/')
            else:
                messages.info(request,"User dosn't exist")
        else:
            messages.info(request,"Invalid Syntaxe")
    form = AuthenticationForm()
    return render(request,"main/Home.html", {"form":form})



def loggedin (request):
    return render(request, "main/Home-Logged.html")