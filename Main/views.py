from django.shortcuts import render
from .models import Publication

# Create your views here.


def post_list(request):

    posts = Publication.objects.all()
    return render(request,'Main/Home.html',{'posts': posts})

