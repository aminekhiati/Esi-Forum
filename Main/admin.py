from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Publication)
admin.site.register(Fichier_attachee)
admin.site.register(Statistiques)
admin.site.register(Commentaire)
admin.site.register(Publication_enrigistre)
admin.site.register(Publication_archivee)

