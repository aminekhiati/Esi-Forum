from django.shortcuts import render, redirect, get_object_or_404
from .models import Publication,Profile,Utilisateur,Commentaire,Report,Message,Category,Tags,Notification
from .forms import (
    SignUpForm,userUpdate,
    approveForm,listuserForm,
    deleteForm,addmodForm,adminUpdate,
    UserUpdateForm,ProfileUpdateForm,
    CommentForm)
from django.conf import settings
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
from django.utils.datastructures import MultiValueDictKeyError


from django.views.generic import (
    CreateView,
    ListView,
    UpdateView,
    DetailView,
    DeleteView
)
import os
from datetime import datetime
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
def admin_loged(user):
    return user.is_authenticated
    



def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
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
            return redirect('home')
        else:
            return redirect('http://127.0.0.1:8000/signup?msg=Email%20Invalid%20Ou%20Username%20Exist!')
        
    else:
        form = SignUpForm()
    return render(request, 'Main/registration.html', {'form': form})




def dashboard(request):

    if not request.user.is_authenticated:
        return redirect('home')
    if  request.user.role!='admin' :
        if request.user.role!='moderateur' :
            return redirect('home')
    queryset = get_current_users()
    pubs_populaie=Publication.objects.annotate(num_c_v=(Count('publication')+F('nb_vues'))).order_by('num_c_v')[0:3]
    nbr_user=Utilisateur.objects.all().count()-1
    nbr_topic=Publication.objects.all().count()
    admin_pubs=Publication.objects.filter(auteur__role='admin')
    reportcnt=Report.objects.all()
    messagecnt=Message.objects.all()
    return render(request, 'Main/admin/Dashboard.html', {"nbr_user":nbr_user,
                                                         "nbr_topic":nbr_topic,
                                                         "pubs_populaie":pubs_populaie,
                                                         "admin_pubs":admin_pubs,
                                                         "nbr_online":queryset.count(),
                                                         "reportcnt":reportcnt,
                                                         "messagecnt":messagecnt

                                                        })

def dashboard_editProfile(request):
    if not request.user.is_authenticated:
        return redirect('home')
    if  request.user.role!='admin' :
        if request.user.role!='moderateur' :
            return redirect('home')
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
                if user.banned:
                    return redirect('http://127.0.0.1:8000/offtalk/?msg=Banned%20User')
                login(request, user)
                messages.success(request, "Logged in successfully as {username}")
                return redirect('home')
            else:
                messages.info(request,"User dosn't exist")
                return redirect('http://127.0.0.1:8000/offtalk/?msg=Invalid%20Login')
        else:
            messages.info(request,"Invalid Syntaxe")
            return redirect('http://127.0.0.1:8000/offtalk/?msg=Invalid%20Login')
    form = AuthenticationForm()
    
    return render(request,"Main/Home-Logged.html", {"form":form})



def loggedin (request):
    return render(request, "Main/Home-Logged.html")


def editeProfile(request):
    u_form = UserUpdateForm()
    user=request.user
    if request.method == 'POST':
        try:
           
            img = request.FILES['image']
            img_extension = os.path.splitext(img.name)[1]
            
            
            user_folder = settings.MEDIA_ROOT+'/profile_pics/'
            print('ok')
            if not os.path.exists(user_folder):
                os.mkdir(user_folder)
            
            img_save_path = user_folder+img.name
     

            with open(img_save_path, 'wb+') as f:
                for chunk in img.chunks():
                    f.write(chunk)
            
            user.profile.image= 'profile_pics/'+img.name
           
            user.save()
        except :
            pass
        pk=user.pk
        user=Utilisateur.objects.filter(id=pk)
        username =request.POST.get('username')
        if username:
            user.update(username=username)
            
        firstname =request.POST.get('firstname')
        if firstname:
            user.update(first_name=firstname)
        
        lastname =request.POST.get('lastname')
        if lastname:
            user.update(last_name=lastname)
        
        email =request.POST.get('email')
        if email:
            user.update(email=email)

        profile=request.user.profile
        phone =request.POST.get('phone')
        if phone:
            profile.numero_telephone=phone

        bio =request.POST.get('bio')
        if bio:
            profile.bio=bio

        password =request.POST.get('password')
        if password:
            if password1:
                if password==password1:
                    user.update(password=password)
        
         

        password =request.POST.get('password')
        if password:
            user.update(password=password)
    user=request.user  
    context ={
        'u_form' : u_form,
        'user' : user
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

def search2(request):
    query =request.GET.get('m')
    essai = Utilisateur.objects.all()
    results = Utilisateur.objects.filter(Q(username__contains=query))

    context ={
        'essai':essai,
        'resutls':results
            }
    return render(request,"Main/searchresults2.html",context)





@login_required()
def userpage(request,pk):
    user = Utilisateur.objects.get(pk=pk)
    context ={
        'user':user
    }
    return render(request,"Main/userpage.html",context)


type_glob  = 'All'
@login_required()
def enrigstre_pub(request,pk):
    request.user.pubs_eng.add(Publication.objects.get(id=pk))
    return redirect('home')
# Publications


class PostListView(ListView):
    model = Publication
    context_object_name = 'posts'
    template_name = 'Main/Home-Logged.html'
    ordering = ['-pk']
    paginate_by = 4

    def get_queryset(self):
        self.category = get_object_or_404(Category,name=self.kwargs['category'])
        global type_glob
        if type_glob != 'All':
            return Publication.objects.filter(category__name=self.category,section=type_glob).order_by('-pk')
        else:
            return Publication.objects.filter(category__name=self.category).order_by('-pk')
    
    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        posts_all = Publication.objects.all()
        comments_all = Commentaire.objects.all()
        users_all = Utilisateur.objects.all()
        students = users_all.filter(role='etudiant')
        professors = users_all.filter(role='enseignant')
        admins = users_all.filter(role='admin')
        moderators = users_all.filter(role='moderateur')
        clubs = users_all.filter(role='clubs')
        popular_topics = Publication.objects.all().order_by('-nb_vues')
        popular_cleared = []
        i = 0
        while i<6 and i<len(popular_topics):
            popular_cleared.append(popular_topics[i])
            i = i +1

        notifications = Notification
        global type_glob
        try:
           page=int(self.request.GET.get('page','1'))
        except ValueError:
           page=1
        if type_glob != 'All':
            posts = Publication.objects.filter(category__name=self.category,section=type_glob).order_by('-pk')
            paginator=Paginator(posts, 4)
            ###...get you page number
            try:
                posts = paginator.page(page)
            except (EmptyPage, InvalidPage):
                posts = paginator.page(paginator.num_pages)
            context.update({
                'posts': posts,
                'category_in': self.category,
                'notifications' : notifications,
                'type_glob' : type_glob,
                'posts_all' : posts_all,
                'comments_all' : comments_all,
                'users_all' : users_all,
                'students' : students,
                'professors' : professors,
                'admins' : admins,
                'moderators' : moderators,
                'popular_cleared' : popular_cleared,
                'clubs' : clubs,
            })
        else:
            posts = Publication.objects.filter(category__name=self.category).order_by('-pk')
            paginator=Paginator(posts, 4)
            try:
                posts = paginator.page(page)
            except (EmptyPage, InvalidPage):
                posts = paginator.page(paginator.num_pages)
            context.update({
                'posts': posts,
                'category_in': self.category,
                'notifications' : notifications,
                'type_glob' : type_glob,
                'posts_all' : posts_all,
                'comments_all' : comments_all,
                'users_all' : users_all,
                'students' : students,
                'professors' : professors,
                'admins' : admins,
                'moderators' : moderators,
                'popular_cleared' : popular_cleared,
                'clubs' : clubs
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
    
    def get_context_data(self, **kwargs):
        global type_glob
        notifications = Notification
        post = self.get_object()
        post.nb_vues = post.nb_vues + 1
        post.save()
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['notifications'] = notifications
        context['type_glob'] = type_glob
        return context
    


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
    fields = ['titre', 'content','section']


    def test_func(self):
        post = self.get_object()
        if self.request.user.role=='admin' or self.request.user.role=='moderateur':
            return True
        else:
            return self.request.user == post.auteur


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Publication
    success_url = '/'


    def test_func(self):
        post = self.get_object()
        if self.request.user.role=='admin' or self.request.user.role=='moderateur':
            return True
        else:
            return self.request.user == post.auteur


#Comments

def add_comment_to_post(request, category ,pk):
    post = get_object_or_404(Publication, pk=pk)
    if request.method == "POST":
        comment = Commentaire()
        notification = Notification()
        notification.user_owner = post.auteur
        comment.publication = post
        content = request.POST['content-comment']
        comment.content = content
        comment.commented_by = request.user
        comment.save()
        notification.comment = comment
        if post.auteur != request.user:
            notification.save()
        return redirect('post-detail',category=post.category.name, pk=post.pk)
    
    return redirect('post-detail',category=post.category.name, pk=post.pk)

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Commentaire
    template_name = 'Main/viewPost.html'
    fields = ['titre', 'content']


    def test_func(self):
        post = self.get_object()
        if self.request.user.role=='admin' or self.request.user.role=='moderateur':
            return True
        else:
            return self.request.user == post.commented_by


@login_required
def comment_remove(request, category,pk1,pk2):
    if request.method == "POST":
        comment = get_object_or_404(Commentaire, pk=pk2)
        if comment.commented_by == request.user or request.user.role=='admin' or request.user.role=='moderateur':
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
        context['banned_list'] = Utilisateur.objects.all().filter(banned=True)
        return context
    def get_queryset(self):
        return Report.objects.all()

class ReportDeleteView(DeleteView):
    template_name = 'Main/admin/MsgsReports.html'
    model = Report
    success_url = '/dashboard/reports/'

class MessageDeleteView(DeleteView):
    template_name = 'Main/admin/MsgsReports.html'
    model = Message
    success_url = '/dashboard/reports/'


def add_message(request):
    if request.method == "POST":
        message = Message()
        if request.user.is_authenticated:
            email = request.user.email
        else:
            email = request.POST.get('email-message')
        content = request.POST['Message-input']
        message.message = content
        message.sybject = 'Message'
        message.email = email
        message.save()

    return redirect('home')



userroleDashboard='all'
usernameDashboard=''

#@login_required(login_url='/home/')
#@user_passes_test(admin_check,login_url='/home/')
class UsersListView(ListView):
    global usernameDashboard
    template_name = 'Main/admin/Users.html'
    context_object_name = 'users_list'
    def get_context_data(self, **kwargs):
        form = userUpdate()
        formm =addmodForm()
        context = super(UsersListView,self).get_context_data(**kwargs)
        context['users_no_list'] = Utilisateur.objects.filter(profile__is_appoved =False)
        context['users_ban_list'] = Utilisateur.objects.filter(banned =True)
        context['students_all_list'] = Utilisateur.objects.filter(role ='etudiant')
        context['enseignant_all_list'] = Utilisateur.objects.filter(role ='enseignant')
        context['clubs_all_list'] = Utilisateur.objects.filter(role ='clubs')
        context['form'] = form
        context['formm'] = formm
        return context
        
    def get_queryset(self):
        print(usernameDashboard)
        user=Utilisateur.objects.filter(profile__is_appoved =True).filter(banned=False)
        if(userroleDashboard!='all'):
            user=user.filter(role =userroleDashboard)
        if(len(usernameDashboard)>1):
            user=Utilisateur.objects.filter(username =usernameDashboard)
            return  user.filter(profile__is_appoved =True)
        else:
            return user



def approverUser(request,pk):
    user=Profile.objects.filter(id=pk).update(is_appoved=True) 
    return redirect('users')
    
def supprimerUser(request,pk):
    Utilisateur.objects.filter(id=pk).delete()
    return redirect('users')

def updateUser(request,pk):   
    user=Utilisateur.objects.get(id=pk)
    if request.method == 'POST':
        try:
            print("okkk")
            img = request.FILES['image']
            img_extension = os.path.splitext(img.name)[1]
            print(img.name)
            print(settings.MEDIA_ROOT)
            user_folder = settings.MEDIA_ROOT+'/profile_pics/'
            print(user_folder)
            if not os.path.exists(user_folder):
                os.mkdir(user_folder)

            img_save_path = user_folder+img.name
            print(img_save_path )

            with open(img_save_path, 'wb+') as f:
                for chunk in img.chunks():
                    f.write(chunk)
        
            user.profile.image= 'profile_pics/'+img.name
            user.save()
        except :
            pass
        user=Utilisateur.objects.filter(id=pk)
        username =request.POST.get('username')
        if username:
            user.update(username=username)
            
        firstname =request.POST.get('firstname')
        if firstname:
            user.update(first_name=firstname)
        
        lastname =request.POST.get('lastname')
        if lastname:
            user.update(last_name=lastname)
        
        email =request.POST.get('email')
        if email:
            user.update(email=email)
         
        role =request.POST.get('role')
        if role:
            user.update(role=role)

        password =request.POST.get('password')
        if password:
            user.update(password=password)
        
               
        
           

    return redirect('users')


def searchUser(request):
    global usernameDashboard
    if request.POST:
        usernameDashboard= request.POST['username']
        print(usernameDashboard)
    return redirect('users')

def selectrole(request):
    global userroleDashboard
    role=request.GET['role']
    userroleDashboard=role;
    print(userroleDashboard)
    return redirect('users')

def addmod(request):   

    if request.method == 'POST':
        user=Utilisateur()
        password =request.POST.get('password')
        password1 =request.POST.get('password1')

        if password:
            if password==password1:
                username =request.POST.get('username')
                if username:
                    user.username=username
            
                firstname =request.POST.get('firstname')
                if firstname:
                    user.first_name=firstname
        
                lastname =request.POST.get('lastname')
                if lastname:
                    user.last_name=lastname
        
                email =request.POST.get('email')
                if email:
                    user.email=email
                user.role = 'moderateur'
                user.save()

        
    
        try:
            print("okkk")
            img = request.FILES['image']
            img_extension = os.path.splitext(img.name)[1]
            print(img.name)
            print(settings.MEDIA_ROOT)
            user_folder = settings.MEDIA_ROOT+'/profile_pics/'
            print(user_folder)
            if not os.path.exists(user_folder):
                os.mkdir(user_folder)

            img_save_path = user_folder+img.name
            print(img_save_path )

            with open(img_save_path, 'wb+') as f:
                for chunk in img.chunks():
                    f.write(chunk)
        
            user.profile.image= 'profile_pics/'+img.name
            user.save()
        except :
            pass

                 
    return redirect('users')

def unban(request,pk):   
    user=Utilisateur.objects.filter(id=pk)
    for us in user:
        us.banned=False
        us.mod=None
        us.subject=None
        us.date=None
        us.duree=0
        us.save()

    return redirect('users')

def ban(request,pk):   
    user=Utilisateur.objects.filter(id=pk)
    if request.method == 'POST':
        reason =request.POST['reason']
        duree =request.POST['duree']
        for us in user:
            us.banned=True
            us.mod=request.user
            us.subject=reason
            us.date=datetime.now()
            us.duree=duree
            us.save()

    return redirect('users')
def redirect_offtalk(request):
    return redirect('category',category='offtalk',)

def clear_notifications(request,category):
    request.user.notifications.all().delete()
    return redirect('category',category='offtalk',)
    

def add_report_post(request, category ,pk):
    post = get_object_or_404(Publication, pk=pk)
    if request.method == "POST":
        report = Report()
        report.from_user = request.user
        report.sybject = request.POST['subject']
        report.reason = request.POST['reason']
        report.user_reported = post.auteur
        report.topic = post
        report.save()
        return redirect('post-detail',category=post.category.name, pk=post.pk)
    
    return redirect('post-detail',category=post.category.name, pk=post.pk)

def add_report_comment(request, category ,pk):
    comment = get_object_or_404(Commentaire, pk=pk)
    if request.method == "POST":
        report = Report()
        report.from_user = request.user
        report.sybject = request.POST['subject']
        report.reason = request.POST['reason']
        report.user_reported = comment.commented_by
        report.topic = comment
        report.save()
        return redirect('post-detail',category=comment.publication.category.name, pk=comment.publication.pk)
    
    return redirect('post-detail',category=comment.publication.category.name, pk=comment.publication.pk)