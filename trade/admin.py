from django.contrib import admin
from .models import Instrument, Bar

# Register your models here.
myModels = [Instrument, Bar]

admin.site.register(myModels)
