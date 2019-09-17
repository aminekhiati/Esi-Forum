from django.db import models
from django.contrib.auth.models import AbstractUser
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.conf import settings    
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User




ROLE = (
        ('etudiant', 'Etudiant'),
        ('enseignant', 'Enseignant'),
        ('moderateur','Moderateur'),
        ('admin','Admin')
    )

PROMO = (
        ('1cpi', '1CPI'),
        ('2cpi', '2CPI'),
        ('1cs', '1CS'),
        ('2cs', '2CS'),
        ('3cs', '3CS'),
    )



class Tags(models.Model):
    name = models.CharField(max_length=20, unique=True)
    slug = models.CharField(max_length=20, unique=True)

    def save(self, *args, **kwargs):
        tempslug = slugify(self.name)
        if self.id:
            tag = Tags.objects.get(pk=self.id)
            if tag.name != self.name:
                self.slug = tempslug
        else:
            self.slug = tempslug
        super(Tags, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Utilisateur(AbstractUser):
    role = models.CharField(choices=ROLE,default='etudiant',max_length=10)

class Publication(models.Model) :
    users = models.ManyToManyField(settings.AUTH_USER_MODEL,related_query_name='users',related_name='pubs_eng',default=None)
    date_de_publication = models.DateField(auto_now_add=True)
    date_de_modification= models.DateField(auto_now=True)
    section = models.CharField(max_length=30)
    content = models.TextField()
    titre = models.CharField(max_length=30)
    auteur = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='publications',related_query_name='auteur')
    tags = models.ManyToManyField(Tags, related_name='posts',default="ok")
    nb_vues =models.IntegerField(default=0)
    

    def __str__(self):
        return self.titre
    
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    

class Profile (models.Model):
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="profile")
    numero_telephone = models.IntegerField(null=True)
    promotion = models.CharField(choices=PROMO,default='1cpi',max_length=4,null=True)
    bio = models.TextField(null=True,blank=True)
    slug = models.SlugField(max_length=250,unique =True,null=True,blank=True)
    publication_enregistrer = models.ForeignKey(Publication,on_delete=models.CASCADE,null=True,blank=True)
    image = models.ImageField(null=True,upload_to='profile_pics',default='profile_pics/default.png')
    is_appoved =models.BooleanField(default=False)

    @receiver(post_save, sender=Utilisateur)
    def update_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()

    def get_absolute_url(self):
        return reverse('Esi_Forum:Main',
        args=[self.user.role,
              self.slug])

    def __str__(self):
        return self.user.username

class Commentaire(models.Model):

    publication = models.ForeignKey(Publication,on_delete =models.CASCADE,related_name="commentaires",related_query_name="publication")
    commented_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name="commentes")
    content = models.TextField(null=True,blank=True)
    date_de_commentaire =  models.DateField(auto_now_add=True)

    def __str__(self):
        return self.publication.titre+ ' commentaire '+ str(self.pk)
    


class Fichier_attachee (models.Model):
    punlication = models.ForeignKey(Publication,on_delete=models.CASCADE)
    commentaire = models.ForeignKey(Commentaire,on_delete=models.CASCADE)

    def __str__(self):
        return self.idfa 


class Report(models.Model):
    from_user = models.ForeignKey(Utilisateur,on_delete=models.CASCADE,related_query_name="user_from")
    sybject = models.TextField(null=True,blank=True)
    date =models.DateField(auto_now_add=True)
    user_reported = models.ForeignKey(Utilisateur,on_delete=models.CASCADE,related_name="report",related_query_name="user_reported")
    reason=models.TextField(null=True,blank=True)
    topic = models.ForeignKey(Publication,on_delete=models.CASCADE)    

class Message(models.Model):
    email=models.EmailField( max_length=254)
    date =models.DateField(auto_now_add=True)
    message=models.TextField(null=True,blank=True)
    sybject = models.TextField(null=True,blank=True)