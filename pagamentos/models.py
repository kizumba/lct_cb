from decimal import Decimal
from django.db import models
from pedidos.models import Pedido, StatusChoices


class FormaPagamento(models.Model):
    nome = models.CharField(max_length=30)
    descricao = models.TextField()

    status = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome


class Pagamento(models.Model):
    pedido = models.ForeignKey(
        Pedido, on_delete=models.PROTECT, related_name="pagamentos")
    forma_pagamento = models.ForeignKey(
        FormaPagamento, on_delete=models.PROTECT, related_name="pagamentos")

    valor_pedido = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal("0.00"))
    valor_pago = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal("0.00"))
    troco = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal("0.00"))

    pago = models.BooleanField(default=False)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):

        # self.valor_pedido = self.pedido.valor_total
        self.valor_pedido = Pedido.objects.get(pk=self.pedido.id).valor_total

        if self.valor_pago > self.valor_pedido:
            self.troco = self.valor_pago - self.valor_pedido
        else:
            self.troco = Decimal("0.00")

        self.pedido = Pedido.objects.get(pk=self.pedido.id)

        if self.pago:
            self.pedido.status = StatusChoices.PAGO
        else:
            self.pedido.status = StatusChoices.PENDENTE

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Pedido: {self.pedido} Valor: {self.valor_pago}"
    
