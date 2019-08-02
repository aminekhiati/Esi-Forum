from django.db import models
from django.contrib.auth.models import User,AbstractUser
from django.template.defaultfilters import slugify

from django.urls import reverse

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



class Publication(models.Model) :

    date_de_publication = models.DateField(auto_now_add=True)
    date_de_modification= models.DateField(auto_now=True)
    section = models.CharField(max_length=30)
    content = models.TextField()
    upvote = models.IntegerField()
    titre = models.CharField(max_length=30)
    lauteur = models.ForeignKey(User,on_delete=models.CASCADE,related_name='publications')
    image_user = models.ImageField() 

    def __str__(self):
        return self.titre

    class Meta:
        ordering = ('-upvote',)


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

class Profile (models.Model):
    
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='userprofile')
    role = models.CharField(choices=ROLE,default='etudiant',max_length=10)
    date_naissance = models.DateField()
    numero_telephone = models.IntegerField()
    promotion = models.CharField(choices=PROMO,default='1cpi',max_length=3)
    bio = models.TextField()
    slug = models.SlugField(max_length=250,unique =True)
    tags = models.ManyToManyField(Tags, related_name='posts')
    publication_enregistrer = models.ForeignKey(Publication,on_delete=models.CASCADE)
    image = models.ImageField()

    def get_absolute_url(self):
        return reverse('Esi_Forum:Main',
        args=[self.role,
              self.user.username,
              self.slug])

    def __str__(self):
        return 'le nom : {} et le prénom : {}'.format(self.user.username,self.user.lastname)





class Commentaire(models.Model):

    publication = models.ForeignKey(Publication,on_delete =models.CASCADE,related_name="commentaires",related_query_name="commentaire")
    commented_by = models.ForeignKey(User,on_delete=models.CASCADE, related_name="commentes")
    content = models.TextField(null=True,blank=True)
    date_de_commentaire =  models.DateField(auto_now_add=True)
    upvote = models.IntegerField()
    date_de_commentaire =  models.DateField(auto_now_add=True)
    tag_utilisateur = models.ManyToManyField(User, related_name="tag_users")
    

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

class Statistiques (models.Model):
    nmbr_publication = models.IntegerField()
    nmbr_commentaires = models.IntegerField()
    nmbr_user   = models.IntegerField()

    def __str__(self):
        return self.ids