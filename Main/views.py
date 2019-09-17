from django.shortcuts import render, redirect, get_object_or_404
from .models import Publication,Profile,Utilisateur,Commentaire,Report,Message,Category,Tags
from .forms import (
    SignUpForm,userUpdate,
    approveForm,listuserForm,
    deleteForm,addmodForm,adminUpdate,
    UserUpdateForm,ProfileUpdateForm,
    CommentForm)
from django.http import HttpResponse
from django.db.models import Count, F, Q
from django.contrib.auth import login, authenticate,logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.forms.models import model_to_dict
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.sessions.models import Session
from django.utils import timezone

from django.views.generic import (
    CreateView,
    ListView,
    UpdateView,
    DetailView,
    DeleteView
)
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger,InvalidPage
def get_current_users():
    active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
    user_id_list = []
    for session in active_sessions:
        data = session.get_decoded()
        user_id_list.append(data.get('_auth_user_id', None))
    # Query all logged in users based on id list
    return Utilisateur.objects.filter(id__in=user_id_list)

def admin_check(user):
    return user.role=="admin" or user.role=="moderateur"



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


@login_required(login_url='/home/')
@user_passes_test(admin_check,login_url='/home/')
def dashboard(request):
    queryset = get_current_users()
    pubs_populaie=Publication.objects.annotate(num_c_v=(Count('publication')+F('nb_vues'))).order_by('num_c_v')[0:3]
    nbr_user=Utilisateur.objects.all().count()-1
    nbr_topic=Publication.objects.all().count()
    admin_pubs=Publication.objects.filter(auteur__role='admin')
    return render(request, 'Main/admin/Dashboard.html', {"nbr_user":nbr_user,
                                                         "nbr_topic":nbr_topic,
                                                         "pubs_populaie":pubs_populaie,
                                                         "admin_pubs":admin_pubs,
                                                         "nbr_online":queryset.count()
                                                        })

@login_required(login_url='/home/')
@user_passes_test(admin_check,login_url='/home/')
def dashboard_editProfile(request):
    form=adminUpdate()
    add = Profile.objects.filter(user__username=request.user)
    for ad in add:
        admin = ad
    if request.method == 'POST' :
        form = adminUpdate(request.POST)
        
        if form.is_valid(): 
            
            if(form.cleaned_data.get('username1')):
                if(form.cleaned_data.get('username')):
                    Utilisateur.objects.filter(username=form.cleaned_data.get('username1')).update(username=form.cleaned_data.get('username'))
                if(form.cleaned_data.get('email')):
                    Utilisateur.objects.filter(username=form.cleaned_data.get('username1')).update(email=form.cleaned_data.get('email'))
                if(form.cleaned_data.get('firstname')):
                    Utilisateur.objects.filter(username=form.cleaned_data.get('username1')).update(first_name=form.cleaned_data.get('firstname'))
                if(form.cleaned_data.get('lastname')):
                    Utilisateur.objects.filter(username=form.cleaned_data.get('username1')).update(first_name=form.cleaned_data.get('last_name'))
     
    
    return render(request, 'Main/admin/EditUser.html', {"admin":admin,
                                                        "form":form
                                                        })

@login_required(login_url='/home/')
@user_passes_test(admin_check,login_url='/home/')
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
    logout(request)
    return redirect('home')




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
                return redirect('home')
            else:
                messages.info(request,"User dosn't exist")
        else:
            messages.info(request,"Invalid Syntaxe")
    form = AuthenticationForm()
    return render(request,"Main/Home-Logged.html", {"form":form})



def loggedin (request):
    return render(request, "Main/Home-Logged.html")


def editeProfile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST,instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES)
        if u_form.is_valid() and p_form.is_valid():
            print("============================================================")
            u_form.save()
            p_form.save(commit=False)
            return HttpResponse('User info changed !')


    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm()

    context ={
        'u_form' : u_form,
        'p_form' : p_form
    }

    return render(request,"Main/usersettings.html",context)


def search(request):
    query =request.GET.get('q')
    essai = Publication.objects.all()
    results = Publication.objects.filter(Q(titre__contains=query))
    context ={
        'essai':essai,
        'resutls':results
    }
    return render(request,"Main/searchresults.html",context)



type_glob  = 'All'
# Publications

class PostListView(ListView):
    model = Publication
    context_object_name = 'posts'
    template_name = 'Main/Home-Logged.html'
    ordering = ['-date_de_publication']
    paginate_by = 4

    def get_queryset(self):
        self.category = get_object_or_404(Category,name=self.kwargs['category'])
        global type_glob
        if type_glob != 'All':
            return Publication.objects.filter(category__name=self.category,section=type_glob)
        else:
            return Publication.objects.filter(category__name=self.category)
    
    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        global type_glob
        try:
           page=int(self.request.GET.get('page','1'))
        except ValueError:
           page=1
        if type_glob != 'All':
            posts = Publication.objects.filter(category__name=self.category,section=type_glob)
            paginator=Paginator(posts, 4)
            ###...get you page number
            try:
                posts = paginator.page(page)
            except (EmptyPage, InvalidPage):
                posts = paginator.page(paginator.num_pages)
            context.update({
                'posts': posts,
                'category_in': self.category,
            })
        else:
            posts = Publication.objects.filter(category__name=self.category)
            paginator=Paginator(posts, 4)
            try:
                posts = paginator.page(page)
            except (EmptyPage, InvalidPage):
                posts = paginator.page(paginator.num_pages)
            context.update({
                'posts': posts,
                'category_in': self.category,
            })
        return context
    
    



def redirect_type(request,category):
    global type_glob 
    category_name = request.get_full_path().split('/')[1]
    type_glob = request.GET['type']
    return redirect('category', category=category_name)

class PostDetailView(DetailView):
    model = Publication
    template_name = 'Main/viewPost.html'
    


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Publication
    template_name = 'Main/Home-Logged.html'
    #fields = ['titre', 'content','section']
    
    def post(self, request, *args, **kwargs):
        category_name = request.get_full_path().split('/')[1]
        post = Publication()
        post.titre = request.POST['titre']
        post.content = request.POST['content']
        post.section = request.POST['section']
        post.category = Category.objects.filter(name=category_name)[0]
        post.auteur = request.user
        post.save()
        return redirect('post-detail', category=category_name, pk=post.id)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Publication
    template_name = 'Main/viewPost.html'
    fields = ['titre', 'content']


    def form_valid(self, form):
        form.instance.auteur = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.auteur


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Publication
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.auteur


#Comments

def add_comment_to_post(request, category ,pk):
    post = get_object_or_404(Publication, pk=pk)
    if request.method == "POST":
        #form = CommentForm(request.POST)
        
        comment = Commentaire()
        comment.publication = post
        content = request.POST['content-comment']
        comment.content = content
        comment.commented_by = request.user
        comment.save()
        return redirect('post-detail',category=post.category.name, pk=post.pk)
    
    return redirect('post-detail',category=post.category.name, pk=post.pk)

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Commentaire
    template_name = 'Main/viewPost.html'
    fields = ['titre', 'content']


    def form_valid(self, form):
        form.instance.auteur = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.commented_by


@login_required
def comment_remove(request, category,pk1,pk2):
    if request.method == "POST":
        comment = get_object_or_404(Commentaire, pk=pk2)
        if comment.commented_by == request.user:
            comment.delete()
            return redirect('post-detail', category=comment.publication.category.name, pk=comment.publication.id)
        else:
            return redirect('post-detail', category=comment.publication.category.name, pk=comment.publication.id)

@login_required
def comment_update(request,category,pk1,pk2):
    post = get_object_or_404(Publication, pk=pk1)
    if request.method == "POST":
        comment = get_object_or_404(Commentaire, pk=pk2)
        if comment.commented_by == request.user:
            comment.publication = post
            content = request.POST['content-comment']
            comment.content = content
            comment.commented_by = request.user
            comment.save()
            return redirect('post-detail', category=comment.publication.category.name, pk=post.pk)
    
    return redirect('post-detail', category=comment.publication.category.name, pk=post.pk)

    
class ReportListView(ListView):
    template_name = 'Main/admin/MsgsReports.html'
    context_object_name = 'reports_list'
    def get_context_data(self, **kwargs):
        context = super(ReportListView, self).get_context_data(**kwargs)
        context['messages_list'] = Message.objects.all()
        return context
    def get_queryset(self):
        return Report.objects.all()

class ReportDeleteView(DeleteView):
    template_name = 'Main/admin/MsgsReports.html'
    model = Report
    success_url = '/reports/'

class MessageDeleteView(DeleteView):
    template_name = 'Main/admin/MsgsReports.html'
    model = Message
    success_url = '/reports/'


def redirect_offtalk(request):
    return redirect('category',category='offtalk',)