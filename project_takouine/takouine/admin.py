from django.contrib import admin

from .models import *

admin.site.register(Edituer),
admin.site.register(Stagiaire),
admin.site.register(Partenaire),
admin.site.register(Achat),
admin.site.register(Visite),
admin.site.register(Formation),
admin.site.register(ContactMessagePartenaire)