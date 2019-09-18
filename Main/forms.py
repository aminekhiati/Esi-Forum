from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Utilisateur,Profile,Commentaire

ROLE = (
        ('etudiant', 'Etudiant'),
        ('enseignant', 'Enseignant'),
    )

ROLE1=(
    ('etudiant', 'Etudiant'),
    ('enseignant', 'Enseignant'),
    ('moderateur','Moderateur')
)

ROLE2=(
    ('All','All'),
    ('etudiant', 'Etudiant'),
    ('enseignant', 'Enseignant'),
    ('moderateur','Moderateur'),
    
)

PROMO = (
        ('1cpi', '1CPI'),
        ('2cpi', '2CPI'),
        ('1cs', '1CS'),
        ('2cs', '2CS'),
        ('3cs', '3CS'),
    )

class SignUpForm(UserCreationForm):

    phone_number=forms.CharField(max_length=10,required=False,label="Phone Number")
    bio =forms.CharField(widget=forms.Textarea,required=False)
    role =forms.ChoiceField(choices = ROLE, label="", initial='', widget=forms.Select(), required=True)
    promo= forms.ChoiceField(choices = PROMO, label="", initial='', widget=forms.Select(), required=True)

    class Meta:
        model = Utilisateur
        fields = ('first_name', 'last_name', 'username', 'email','phone_number', 'password1', 'password2', 'role','promo','bio')



class userUpdate(forms.Form):
    firstname=forms.CharField(required=False)
    lastname=forms.CharField(required=False)
    username=forms.CharField(required=False)
    username1=forms.CharField(required=False)
    role =forms.ChoiceField(choices = ROLE1, widget=forms.Select(), required=False)
    password =forms.CharField(required=False)
    password1 =forms.CharField(required=False)
    email= forms.EmailField(required=False)
    image=forms.ImageField(required=False)
    
    def clean(self):
        cd = self.cleaned_data
        username=cd.get('username')
        email=cd.get('email')
        a_string = email[-10:]
        print(a_string)
        if cd.get('password') != cd.get('password1'):
            self.add_error('password1', "passwords do not match !")
        if  (Utilisateur.objects.filter(username=username).count()>0):
            self.add_error('username', "username exist !")

        if  (a_string!='esi-sba.dz'):
            self.add_error('email', "email aint from school  !")
        



class approveForm(forms.Form):
    username=forms.CharField(required=True)

class listuserForm(forms.Form):
    select=forms.ChoiceField(choices=ROLE2, required=False)
    
class deleteForm(forms.Form):
    username=forms.CharField(required=True)       

class addmodForm(forms.Form):
    firstname=forms.CharField(required=True)
    lastname=forms.CharField(required=True)
    username=forms.CharField(required=True)
    password =forms.CharField(required=True)
    password1 =forms.CharField(required=True)
    email= forms.EmailField(required=True)
    image=forms.ImageField(required=False)

    def clean(self):
        cd = self.cleaned_data
        username=cd.get('username')
        email=cd.get('email')
        a_string = email[-10:]
        print(a_string)
        if cd.get('password') != cd.get('password1'):
            self.add_error('password1', "passwords do not match !")
        if  (Utilisateur.objects.filter(username=username).count()>0):
            self.add_error('username', "username exist !")


class adminUpdate(forms.Form):
    firstname=forms.CharField(required=False)
    lastname=forms.CharField(required=False)
    username=forms.CharField(required=False)
    username1=forms.CharField(required=False)
    password =forms.CharField(required=False)
    password1 =forms.CharField(required=False)
    email= forms.EmailField(required=False)


    def clean(self):
        cd = self.cleaned_data
        if cd.get('password') != cd.get('password1'):
            self.add_error('passwor1', "passwords do not match !")
       
        return cd

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    image=forms.ImageField()


    class Meta:
        model = Utilisateur
        fields = (
            'first_name', 'last_name', 'username', 'email', 'password','image')
            

class ProfileUpdateForm(forms.ModelForm):
    nt = forms.CharField(max_length=10, required=False, label="Phone Number")
    promo = forms.ChoiceField(choices=PROMO, label="", initial='', widget=forms.Select(), required=False)

    class Meta:
        model = Profile
        fields = ('nt','promo'
            )

class CommentForm(forms.ModelForm):
    content = forms.CharField( widget=forms.Textarea )
    class Meta:
        model = Commentaire
        fields = ('content',)
