from django.contrib import admin

from usuarios.models import Usuario, TipoUsuario, UsuarioTipoUsuario, Endereco


class UsuarioAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "user", "cpf",
                    "telefone", "data_nascimento", "status",)
    search_fields = ("nome",)
    list_editable = ("status",)


# class TipoUsuarioAdmin(admin.ModelAdmin):
#     list_display = ("nome",)
#     search_fields = ("nome", )


class EnderecoAdmin(admin.ModelAdmin):
    list_display = ("usuario", "nome", "logradouro", "numero",
                    "bairro", "cidade", "uf", "principal",)
    search_fields = ("nome",)


admin.site.register(Usuario, UsuarioAdmin)
# admin.site.register(TipoUsuario, TipoUsuarioAdmin)
# admin.site.register(UsuarioTipoUsuario)
admin.site.register(Endereco, EnderecoAdmin)
