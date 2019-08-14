from django.shortcuts import render, redirect
from .models import Publication,Profile,Utilisateur
from .forms import SignUpForm,userUpdate,approveForm,listuserForm,deleteForm,addmodForm
from django.http import HttpResponse
from django.db.models import Count, F
from django.contrib.auth import login, authenticate,logout
from django.forms.models import model_to_dict
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Publication
from django.views.generic import (
    CreateView,
    ListView,
    UpdateView,
    DetailView,
    DeleteView
)


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
            utilisateur.profile.is_appoved =False
            #username = form.cleaned_data.get('username')
            #raw_password = form.cleaned_data.get('password1')
            #user = authenticate(username=username, password=raw_password)
            #login(request, user)
            utilisateur.save()
            return HttpResponse('success')
    else:
        form = SignUpForm()
    return render(request, 'Main/registration.html', {'form': form})



def dashboard(request):
    pubs_populaie=Publication.objects.annotate(num_c_v=(Count('commentaire')+F('nb_vues'))).order_by('num_c_v')[0:3]
    nbr_user=Utilisateur.objects.all().count()-1
    nbr_topic=Publication.objects.all().count()
    return render(request, 'Main/admin/Dashboard.html', {"nbr_user":nbr_user,
                                                         "nbr_topic":nbr_topic,
                                                         "pubs_populaie":pubs_populaie
                                                        })
def dashboard_editProfile(request):
    admin=Profile.objects.all()[0:1]
    return render(request, 'Main/admin/EditUser.html', {"admin":admin,
                                                        })


def users(request):
    if request.method == 'POST' and 'update' in request.POST:
        form = userUpdate(request.POST)
        
        if form.is_valid(): 
            print('hhh')
            if(form.cleaned_data.get('username1')):
                if(form.cleaned_data.get('username')):
                    Utilisateur.objects.filter(username=form.cleaned_data.get('username1')).update(username=form.cleaned_data.get('username'))
                if(form.cleaned_data.get('email')):
                    Utilisateur.objects.filter(username=form.cleaned_data.get('username1')).update(email=form.cleaned_data.get('email'))
                if(form.cleaned_data.get('password')):
                    Utilisateur.objects.filter(username=form.cleaned_data.get('username1')).update(password=form.cleaned_data.get('password'))
                
                Utilisateur.objects.filter(username=form.cleaned_data.get('username1')).update(role=form.cleaned_data.get('role'))

            return HttpResponse('success')
    if request.method=='POST' and 'approve' in request.POST:
            formp =approveForm(request.POST)
            if formp.is_valid():
                
                if(formp.cleaned_data.get('username')):
                    print("ok")
                    profile=Profile.objects.filter(user__username=formp.cleaned_data.get('username'))
                    profile.update(is_appoved=True)
    users=Profile.objects.filter(is_appoved=True) 
    if request.method=='POST' and 'selectt' in request.POST:
            forms =listuserForm(request.POST)
            if forms.is_valid():              
                if forms.cleaned_data.get('select') == 'All':
                    users=Profile.objects.filter(is_appoved=True)
                elif forms.cleaned_data.get('select') == 'enseignant':
                    users=Profile.objects.filter(is_appoved=True).filter(user__role="enseignant")
                elif forms.cleaned_data.get('select') == 'etudiant':
                    users=Profile.objects.filter(is_appoved=True).filter(user__role="etudiant")
                elif forms.cleaned_data.get('select') == 'moderateur':
                    users=Profile.objects.filter(is_appoved=True).filter(user__role="moderateur")

    if request.method=='POST' and 'delete' in request.POST:
            formd =deleteForm(request.POST)
            if formd.is_valid():              
               Utilisateur.objects.filter(username=formd.cleaned_data.get('username')).delete()

    if request.method == 'POST' and 'addmod' in request.POST:
        formadd = addmodForm(request.POST)
        if formadd.is_valid():
            Utilisateur.objects.create(username=formadd.cleaned_data.get('username'), email=formadd.cleaned_data.get('email'),password=formadd.cleaned_data.get('password'),role="moderateur")
            
            
    formadd=addmodForm(request.POST)
    formdelete=deleteForm()
    formselect=listuserForm()
    formusers = userUpdate() 
    formuserno=approveForm()
    nbstd=Utilisateur.objects.filter(role="etudiant").count()
    nbprof=Utilisateur.objects.filter(role="enseignant").count()
    nbpmod=Utilisateur.objects.filter(role="moderateur").count()
    usersNo=Profile.objects.filter(is_appoved=False)
    return render(request, 'Main/admin/Users.html', {"usersNo":usersNo,
                                                     "users":users,
                                                      "formusers":formusers,
                                                      "formuserno":formuserno,
                                                      "formselect":formselect,
                                                      "formdelete":formdelete,
                                                      "formadd":formadd,
                                                      "nbstd":nbstd,
                                                      "nbprof":nbprof,
                                                      "nbpmod":nbpmod,
                                                        })    
               

def logout_request(request):
    print("sjaspasasas")
    logout(request)
    messages.info(request,"Logged out successfully")
    return redirect('../login')

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Logged in successfully as {username}")
                return redirect('../home/')
            else:
                messages.info(request,"User dosn't exist")
        else:
            messages.info(request,"Invalid Syntaxe")
    form = AuthenticationForm()
    return render(request,"Main/Home.html", {"form":form})



def loggedin (request):
    return render(request, "Main/Home-Logged.html")


def editeProfile(request):
    return render(request,"Main/usersettings.html")


# <app>/<model>_<viewtype>.html <-- template naming conventions for best practice

class PostListView(LoginRequiredMixin, ListView):
    model = Publication
    context_object_name = 'Publication'
    template_name = 'Main/Home-Logged.html'
    ordering = ['-date_de_publication']


class PostDetailView(LoginRequiredMixin, DetailView):
    model = Publication
    context_object_name = 'Publication'
    template_name = 'Main/viewPost.html'


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Publication
    fields = ['titre', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Publication
    fields = ['titre', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # prevent any users from editing people's posts --> devrait retourner une erreure 403 (i.e forbidden)
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.lauteur


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Publication
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.lauteur
