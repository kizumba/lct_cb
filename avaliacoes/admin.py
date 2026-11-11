from django.contrib import admin

from .models import Avaliacao

@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ("pedido", "usuario", "nota", "data_criacao")
    list_filter = ("nota", "data_criacao")
    search_fields = ("pedido__id", "usuario", "comentario")
    
