from django.db import models


# Create your models here.
class Entregador(models.Model):
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20, null=True, blank=True)
    chave_pix = models.CharField(max_length=200, null=True, blank=True)
    status = models.BooleanField(default=True)
    
    class Meta:
        # Nome exibido no singular
        verbose_name = "Entregador"
        
        # Nome exibido no plural (o Django costuma apenas adicionar um "s" por padrão)
        verbose_name_plural = "Entregadores"

    def __str__(self):
        return self.nome
    