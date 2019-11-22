from django.contrib import admin
from .models import Instrument, Bar


class BarAdmin(admin.ModelAdmin):
    list_display = ['instrument', 'timeframe', 'time', 'created_by']
    list_display_links = ['instrument']
    search_fields = ['instrument']
    list_filter = ['timeframe']


class InstrumentAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_by']
    list_display_links = ['name']
    search_fields = ['name']

# Register your models here.
myModels = [Bar, BarAdmin]

admin.site.register(Bar, BarAdmin)
admin.site.register(Instrument, InstrumentAdmin)
