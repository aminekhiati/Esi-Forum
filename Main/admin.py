from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Profile)
admin.site.register(Publication)
admin.site.register(Fichier_attachee)
admin.site.register(Commentaire)
admin.site.register(Publication_archivee)
admin.site.register(Utilisateur)
admin.site.register(Tags)
admin.site.register(Report)
admin.site.register(Message)


