from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from django.template.defaultfilters import pluralize
from datetime import datetime, timedelta, timezone
from urllib.parse import urlparse


class Profile(models.Model):
    ROLE = (
        ('etudiant', 'Etudiant'),
        ('enseignant', 'Enseignant'),
        ('moderateur', 'Moderateur')
    )

    PROMO = (
        ('1cpi', '1CPI'),
        ('2cpi', '2CPI'),
        ('1cs', '1CS'),
        ('2cs', '2CS'),
        ('3cs', '3CS'),
    )

    user = models.OneToOneField \
        (User,
         on_delete=models.CASCADE,
         related_name='userprofile'
         )
    role = models.CharField \
        (choices=ROLE,
         default='etudiant',
         max_length=10
         )
    date_naissance = models.DateField()
    numero_telephone = models.IntegerField()
    promotion = models.CharField \
        (choices=PROMO,
         default='1cpi',
         max_length=3
         )
    bio = models.TextField()
    slug = models.SlugField \
        (max_length=250,
         unique=True)

    def get_absolute_url(self):
        return reverse('Esi_Forum:Main',
                       args=[self.user.role,
                             self.user.username,
                             self.slug])

    def __str__(self):
        return 'le nom : {} et le prénom : {}'.format(self.user.username, self.user.lastname)


class Publication(models.Model):
    date_de_publication = models.DateField \
        (auto_now_add=True,
         )
    date_de_modification = models.DateField \
        (auto_now=True
         )
    section = models.CharField(max_length=30)
    text = models.TextField()

    upvotes = models.ManyToManyField \
        (User,
         through='PublicationUpvote'
         )
    title = models.CharField(max_length=256)
    lauteur = models.ForeignKey \
        (User,
         on_delete=models.SET_NULL,
         related_name='publications'
         )  # when a user is deleted we keep the posts and the creator is set to null
    ''' photo = models.ImageField() '''
    ''' categorie = models.ForeignKey()'''

    def how_long_ago(self):
        how_long = datetime.now(timezone.utc) - self.creation_date
        if how_long < timedelta(minutes=1):
            return f'{how_long.seconds} second{pluralize(how_long.seconds)} ago'
        elif how_long < timedelta(hours=1):
            # total_seconds returns a float
            minutes = int(how_long.total_seconds()) // 60
            return f'{minutes} minute{pluralize(minutes)} ago'
        elif how_long < timedelta(days=1):
            hours = int(how_long.total_seconds()) // 3600
            return f'{hours} hour{pluralize(hours)} ago'
        else:
            return f'{how_long.days} day{pluralize(how_long.days)} ago'

    def set_upvoted(self, user, *, upvoted):
        if upvoted:
            PublicationUpvote.objects.get_or_create(post=self, user=user)
        else:
            self.upvotes.filter(id=user.id).delete()

    def __str__(self):
        return self.titre

    class Meta:
        ordering = ('-upvote',)


class PublicationUpvote(models.Model):
    post = models.ForeignKey \
            (
            Publication,
            on_delete=models.CASCADE,
        )  # remove the upvote when the post is deleted
    user = models.ForeignKey \
            (
            User,
            related_name='upvotes',
            on_delete=models.CASCADE,
        )  # remove the upvote when the user is deleted

    class Meta:
        unique_together = ('publication', 'user')


class Commentaire(models.Model):
    creator = models.ForeignKey \
        (User,
         related_name='comments',
         # when the creator is removed set creator to null
         on_delete=models.SET_NULL,
         null=True,
         )
    publication = models.ForeignKey \
        (Publication,
         related_name="comments",
         on_delete=models.CASCADE
         # when post is removed there is no way to read the comments so we just remove them
         )
    parent = models.ForeignKey \
            (
            # What happens when the parent is removed? It should never be removed
            # otherwise the comment tree will be messed up.
            # We’ll just set the content to
            'Comment',
            related_name='replies',
            on_delete=models.CASCADE,
            null=True,
            default=None,
        )
    text = models.TextField(null=True, blank=True)
    upvotes = models.ManyToManyField \
        (User,
         through='CommentUpvote'
         )
    date_de_commentaire = models.DateField(auto_now_add=True)
    tag_utilisateur = models.ManyToManyField \
        (User,
         related_name="tag_users"
         )

    def set_upvoted(self, user, *, upvoted):
        if upvoted:
            CommentUpvote.objects.get_or_create(comment=self, user=user)
        else:
            self.upvotes.filter(id=user.id).delete()

    def __str__(self):
        return self.pk


class CommentUpvote(models.Model):
    comment = models.ForeignKey \
            (
            Commentaire,
            on_delete=models.CASCADE,
        )  # remove the upvote when the comment is deleted
    user = models.ForeignKey \
            (
            User,
            related_name='comment_upvotes',
            on_delete=models.CASCADE,
        )  # remove the upvote when the user is deleted

    class Meta:
        unique_together = ('comment', 'user')


class Publication_enrigistre(models.Model):
    idpe = models.IntegerField(primary_key=True)
    idu = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.idpe


class Publication_archivee(models.Model):
    idpa = models.IntegerField(primary_key=True)

    def __str__(self):
        return self.idpa


class Fichier_attachee(models.Model):
    idfa = models.IntegerField(primary_key=True)
    idp = models.ForeignKey(Publication, on_delete=models.CASCADE)
    idc = models.ForeignKey(Commentaire, on_delete=models.CASCADE)

    def __str__(self):
        return self.idfa


class Statistiques(models.Model):
    ids = models.IntegerField(primary_key=True)
    nmbr_publication = models.IntegerField()
    nmbr_commentaires = models.IntegerField()
    upvote = models.IntegerField()

    def __str__(self):
        return self.ids