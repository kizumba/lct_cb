from django.db import models

from pedidos.models import Pedido
from usuarios.models import Usuario

class Avaliacao(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="avaliacoes")
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="avaliacoes")
    nota = models.IntegerField()
    comentario = models.TextField(blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Avaliação do pedido {self.pedido.id} por {self.usuario}"
