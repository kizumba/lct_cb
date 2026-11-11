from decimal import Decimal
from django.db import models
from usuarios.models import Usuario
from entregadores.models import Entregador
from produtos.models import Produto

from usuarios.models import Usuario, Endereco as EnderecoUsuario


class EnderecoPedido(models.Model):
    logradouro = models.CharField(max_length=100, null=True, blank=True)
    numero = models.CharField(max_length=6, null=True, blank=True)
    bairro = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.logradouro}, {self.numero}, {self.bairro}"


class StatusChoices(models.TextChoices):
    CARRINHO = "Carrinho", "Carrinho"
    PENDENTE = "Pendente", "Pendente"
    PAGO = "Pago", "Pago"
    ENVIADO = "Enviado", "Enviado"
    CANCELADO = "Cancelado", "Cancelado"


class Pedido(models.Model):
    valor_subtotal = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal("0.00"))
    taxa_entrega = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal("0.00"))
    desconto = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal("0.00"))
    valor_total = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal("0.00"))
    observacao = models.TextField(null=True, blank=True)

    status = models.CharField(
        max_length=10, choices=StatusChoices.choices, default=StatusChoices.CARRINHO)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    usuario = models.ForeignKey(
        Usuario, on_delete=models.CASCADE, related_name="pedidos")
    entregador = models.ForeignKey(
        Entregador, on_delete=models.CASCADE, related_name="pedidos")
    endereco = models.ForeignKey(
        EnderecoPedido, on_delete=models.PROTECT, related_name="pedidos", null=True, blank=True)

    # def save(self, *args, **kwargs):
    #     subtotal = self.valor_subtotal or Decimal("0.00")
    #     taxa = self.taxa_entrega or Decimal("0.00")
    #     desc = self.desconto or Decimal("0.00")
    #     self.valor_total = subtotal + taxa - desc

    #     super().save(*args, **kwargs)

    def save(self, *args, **kwargs):
        subtotal = self.valor_subtotal or Decimal("0.00")
        taxa = self.taxa_entrega or Decimal("0.00")
        desc = self.desconto or Decimal("0.00")
        self.valor_total = subtotal + taxa - desc

        if self.usuario_id:
            # Pega o endereço principal do usuário; se não houver, o primeiro
            endereco_usuario = (
                EnderecoUsuario.objects.filter(
                    usuario_id=self.usuario_id, principal=True).first()
                or EnderecoUsuario.objects.filter(usuario_id=self.usuario_id).first()
            )

            if endereco_usuario:
                if self.endereco_id is None:
                    # Cria o endereço do pedido (snapshot) a partir do usuário
                    self.endereco = EnderecoPedido.objects.create(
                        logradouro=endereco_usuario.logradouro,
                        numero=endereco_usuario.numero,
                        bairro=endereco_usuario.bairro,
                    )
                else:
                    # Sincroniza o endereço já existente do pedido
                    self.endereco.logradouro = endereco_usuario.logradouro
                    self.endereco.numero = endereco_usuario.numero
                    self.endereco.bairro = endereco_usuario.bairro
                    self.endereco.save()

        super().save(*args, **kwargs)

        if self.pagamentos.exists():
            # Se houver pagamentos, atualiza o valor do pedido nos pagamentos
            
            for pagamento in self.pagamentos.all():
                self.status = StatusChoices.PAGO if pagamento.pago else StatusChoices.PENDENTE
                pagamento.valor_pedido = self.valor_total
                pagamento.save()

            super().save(*args, **kwargs)

    def __str__(self):
        cpf = self.usuario.cpf if self.usuario else "Sem usuário"
        return f"Pedido: {self.id}"


class ItemPedido(models.Model):
    pedido = models.ForeignKey(
        Pedido, on_delete=models.CASCADE, related_name="item_pedido")
    produto = models.ForeignKey(
        Produto, on_delete=models.CASCADE, related_name="item_pedido")
    preco_unitario = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    quantidade = models.IntegerField(default=1)
    observacao = models.TextField(null=True, blank=True)
    preco_total = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal("0.00"))
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def calcular_total(self):
        base = (self.preco_unitario or Decimal(
            "0.00")) * (self.quantidade or 1)

        # Puxa os adicionais direto do banco de dados
        if self.pk:
            total_adicionais = sum(
                (a.preco_total or Decimal("0.00")
                 for a in self.adicionais.all()),
                Decimal("0.00")
            )
        else:
            total_adicionais = Decimal("0.00")

        return base + total_adicionais

    def save(self, *args, **kwargs):
        if self.preco_unitario is None and self.produto_id:
            self.preco_unitario = self.produto.valor

        self.preco_total = self.calcular_total()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Pedido: {self.pedido.id} - Item: {self.id} - Produto: {self.produto.nome}"


class Adicional(models.Model):
    nome = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.BooleanField(default=True)

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome


class ItemAdicional(models.Model):
    adicional = models.ForeignKey(
        Adicional, on_delete=models.PROTECT, related_name="adicionais")
    item_pedido = models.ForeignKey(
        ItemPedido, on_delete=models.PROTECT, related_name="adicionais")

    preco_unitario = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    quantidade = models.IntegerField(default=1)
    preco_total = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal("0.00"))

    def save(self, *args, **kwargs):
        if self.preco_unitario is None and self.adicional_id:
            self.preco_unitario = self.adicional.valor

        preco = self.preco_unitario or Decimal("0.00")
        quantidade = self.quantidade or 1
        self.preco_total = preco * quantidade

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.adicional.nome} x {self.quantidade} (item {self.item_pedido.id})"
