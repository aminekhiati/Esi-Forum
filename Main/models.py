from django.db import models

# Create your models here.

class Utilisateur (models.Model):
    idu = models.IntegerField(primary_key=True)

    def __str__(self):
        return self.idu

class Compte (models.Model):
    idu = models.IntegerField(primary_key=True)
    nom_utilisateur = models.CharField(max_length=30)
    email = models.EmailField()
    password = models.CharField(max_length=30)

    def __str__(self):
        return self.nom_utilisateur

class Profile (models.Model):
    idpr = models.IntegerField(primary_key=True)
    nom = models.CharField(max_length=30)
    prenom = models.CharField(max_length=30)
    date_naissance = models.DateField
    numero_telephone = models.IntegerField
    role = models.CharField(max_length=30)
    promotion = models.CharField(max_length=30)
    bio = models.TextField()

    def __str__(self):
        return self.nom+' '+self.prenom

class Administration (models.Model):
    ida = models.IntegerField(primary_key=True)

    def __str__(self):
        return self.ida

class Publication(models.Model) :
    idp = models.IntegerField(primary_key=True)
    date = models.DateField()
    section = models.CharField(max_length=30)
    text = models.TextField()
    upvote = models.IntegerField
    titre = models.CharField(max_length=30)
    idu = models.ForeignKey(Utilisateur,on_delete=models.CASCADE)
    ida = models.ForeignKey(Administration,on_delete=models.CASCADE)

    def __str__(self):
        return self.titre

class Commentaire(models.Model):
    idc = models.IntegerField(primary_key=True)
    date = models.DateField()
    section = models.CharField(max_length=30)
    text = models.TextField()
    upvote = models.IntegerField
    titre = models.CharField(max_length=30)
    idu = models.ForeignKey(Utilisateur,on_delete=models.CASCADE)
    ida = models.ForeignKey(Administration,on_delete=models.CASCADE)
    idp = models.ForeignKey(Publication,on_delete=models.CASCADE)

    def __str__(self):
        return self.titre

class Moderateur (models.Model):
    idm = models.IntegerField(primary_key=True)
    ida = models.ForeignKey(Administration,on_delete=models.CASCADE)

    def __str__(self):
        return self.id

class Publication_enrigistre(models.Model):
    idpe = models.IntegerField(primary_key=True)
    idu = models.ForeignKey(Utilisateur,on_delete=models.CASCADE)

    def __str__(self):
        return self.idpe

class Publication_archivee(models.Model):
    idpa =models.IntegerField(primary_key=True)

    def __str__(self):
        return self.idpa

class Fichier_attachee (models.Model):
    idfa = models.IntegerField(primary_key=True)
    idp = models.ForeignKey(Publication,on_delete=models.CASCADE)
    idc = models.ForeignKey(Commentaire,on_delete=models.CASCADE)

    def __str__(self):
        return self.idfa

class Statistiques (models.Model):
    ids = models.IntegerField(primary_key=True)
    nmbr_publication = models.IntegerField()
    nmbr_commentaires = models.IntegerField()
    upvote = models.IntegerField()

    def __str__(self):
        return self.ids