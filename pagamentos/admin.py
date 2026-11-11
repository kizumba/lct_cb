from django.contrib import admin

from pagamentos.models import Pagamento, FormaPagamento


@admin.register(Pagamento)
class PagamentoAdmin(admin.ModelAdmin):
    list_display = ("pedido", "forma_pagamento",
                    "valor_pago", "troco", "valor_pedido",
                    "criado_em",
                    "atualizado_em",
                    "pago"
                    )
    search_fields = ("pedido", )


@admin.register(FormaPagamento)
class FormaPagamentoAdmin(admin.ModelAdmin):
    list_display = (
        "nome",
        "descricao",
        "criado_em",
        "atualizado_em"
    )
    search_fields = ("nome", )