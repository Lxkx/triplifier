from django.contrib import admin

from triplifierapp.models import csvModel, ttlModel

admin.site.register(csvModel)
admin.site.register(ttlModel)

# Register your models here.
