from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Utilisateur

ROLE = (
        ('etudiant', 'Etudiant'),
        ('enseignant', 'Enseignant'),
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