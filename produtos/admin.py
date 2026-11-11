from django.contrib import admin

from produtos.models import Produto, Categoria


class ProdutoAdmin(admin.ModelAdmin):
    list_display = ("nome", "descricao", "valor",)
    search_fields = ("nome",)


class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nome", "descricao",)
    search_fields = ("nome", )


admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Categoria, CategoriaAdmin)
