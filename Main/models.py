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
        ('moderateur','Moderateur')
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

    date_de_publication = models.DateField(auto_now_add=True)
    date_de_modification= models.DateField(auto_now=True)
    section = models.CharField(max_length=30)
    content = models.TextField()
    upvote = models.IntegerField()
    titre = models.CharField(max_length=30)
    lauteur = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='publications')
    image = models.ImageField(null=True) 
    tags = models.ManyToManyField(Tags, related_name='posts',default="ok")
    nb_vues =models.IntegerField(default=0)
    

    def __str__(self):
        return self.titre

    class Meta:
        ordering = ('-upvote',)

class Profile (models.Model):
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="profile")
    numero_telephone = models.IntegerField(null=True)
    promotion = models.CharField(choices=PROMO,default='1cpi',max_length=4,null=True)
    bio = models.TextField(null=True)
    slug = models.SlugField(max_length=250,unique =True,null=True,blank=True)
    publication_enregistrer = models.ForeignKey(Publication,on_delete=models.CASCADE,null=True,blank=True)
    image = models.ImageField(null=True,upload_to='profile_pics')
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

    publication = models.ForeignKey(Publication,on_delete =models.CASCADE,related_name="commentaires",related_query_name="commentaire")
    commented_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name="commentes")
    content = models.TextField(null=True,blank=True)
    date_de_commentaire =  models.DateField(auto_now_add=True)
    upvote = models.IntegerField()
    date_de_commentaire =  models.DateField(auto_now_add=True)
    tag_utilisateur = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="tag_users")
    

    def __str__(self):
        return self.pk



class Publication_archivee(models.Model):

    def __str__(self):
        return self.idpa 

class Fichier_attachee (models.Model):
    punlication = models.ForeignKey(Publication,on_delete=models.CASCADE)
    commentaire = models.ForeignKey(Commentaire,on_delete=models.CASCADE)

    def __str__(self):
        return self.idfa 


