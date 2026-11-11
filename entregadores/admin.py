from django.contrib import admin

from entregadores.models import Entregador

class EntregadorAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "telefone", "chave_pix", "status", )
    search_fields = ("nome", )
    list_editable = ("status", )


admin.site.register(Entregador, EntregadorAdmin)
