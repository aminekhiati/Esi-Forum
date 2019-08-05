from django.shortcuts import render, redirect
from .models import Publication
from .forms import SignUpForm
from django.http import HttpResponse



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


