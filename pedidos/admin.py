from django.contrib import admin
from decimal import Decimal

from pedidos.models import Pedido, ItemPedido, Adicional, ItemAdicional

from pagamentos.models import Pagamento


class PagamentoInline(admin.TabularInline):
    model = Pagamento
    extra = 0
    autocomplete_fields = ("forma_pagamento",)
    readonly_fields = ("valor_pedido",
                       "troco", "criado_em", "atualizado_em")


class ItemAdicionalInline(admin.TabularInline):
    model = ItemAdicional
    extra = 1
    autocomplete_fields = ("adicional",)
    readonly_fields = ("preco_total", "preco_unitario")


class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 1
    search_fields = ("pedido__id", "produto__nome")
    readonly_fields = ("preco_total", "preco_unitario", "observacao")
    autocomplete_fields = ("produto",)


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = (
        "id", "valor_total", "valor_subtotal", "taxa_entrega",
        "desconto", "status", "criado_em", "usuario",
    )
    list_filter = ("status", "criado_em",)
    search_fields = ("usuario__cpf", "id",)

    readonly_fields = (
        "valor_subtotal", "valor_total",
        "criado_em", "atualizado_em",
        "endereco_logradouro",
        "endereco_numero",
        "endereco_bairro",
    )

    inlines = [ItemPedidoInline, PagamentoInline]

    fieldsets = (
        ("Cliente e Entregador", {
            "fields": ("usuario", "entregador", "status")
        }),
        ("Valores", {
            "fields": ("valor_subtotal", "taxa_entrega", "desconto", "valor_total")
        }),
        ("Endereço de  Entrega", {
            "fields": ("endereco_logradouro", "endereco_numero", "endereco_bairro")
        }),
        ("Outros", {
            "fields": ("observacao", "criado_em", "atualizado_em")
        }),
    )

    def endereco_logradouro(self, obj):
        return obj.endereco.logradouro if obj.endereco else "-"
        endereco_logradouro.short_description = "Logradouro"

    def endereco_numero(self, obj):
        return obj.endereco.numero if obj.endereco else "-"
        endereco_numero.short_description = "Número"

    def endereco_bairro(self, obj):
        return obj.endereco.bairro if obj.endereco else "-"
        endereco_bairro.short_description = "Bairro"

    def save_related(self, request, form, formsets, change):
        # 1. Salva os itens do inline
        super().save_related(request, form, formsets, change)

        pedido = form.instance

        # 2. Soma o total de todos os itens salvos
        pedido.valor_subtotal = sum(
            (item.preco_total or Decimal("0.00")
             for item in pedido.item_pedido.all()),
            Decimal("0.00")
        )

        # 3. Salva o pedido (o save() vai calcular o valor_total correto)
        pedido.save()

        # 4. Atualiza a tela do Admin
        form.instance.refresh_from_db()


@admin.register(ItemPedido)
class ItemPedidoAdmin(admin.ModelAdmin):
    list_display = ("id", "pedido", "produto", "quantidade",
                    "preco_unitario", "preco_total")
    list_filter = ("criado_em",)
    search_fields = ("pedido__id", "produto__nome")
    autocomplete_fields = ("pedido", "produto")
    inlines = [ItemAdicionalInline]

    def save_related(self, request, form, formsets, change):
        # 1. Salva os adicionais
        super().save_related(request, form, formsets, change)

        item = form.instance

        # 2. Recalcula o total do item (base + adicionais)
        item.preco_total = item.calcular_total()
        item.save()

        # 3. Atualiza o Pedido pai (soma todos os itens novamente)
        pedido = item.pedido
        pedido.valor_subtotal = sum(
            (i.preco_total or Decimal("0.00")
             for i in pedido.item_pedido.all()),
            Decimal("0.00")
        )
        pedido.save()

        # 4. Atualiza a tela do Admin
        item.refresh_from_db()


@admin.register(Adicional)
class AdicionalAdmin(admin.ModelAdmin):
    list_display = ("id", "nome", "valor", "status")
    search_fields = ("nome", )
    list_filter = ("status",)


@admin.register(ItemAdicional)
class ItemAdicionalAdmin(admin.ModelAdmin):
    list_display = ("id", "adicional", "item_pedido",
                    "quantidade", "preco_total")
    search_fields = ("id", "adicional__nome")
