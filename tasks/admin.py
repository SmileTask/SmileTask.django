from django.contrib import admin
from .models import tareas

class adminTareas(admin.ModelAdmin):
    readonly_fields = ('created', )

# Register your models here.
admin.site.register(tareas, adminTareas)