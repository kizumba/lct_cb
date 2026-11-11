from django.db import models


class Categoria(models.Model):
    nome = models.CharField(max_length=100, null=False, blank=False)
    descricao = models.TextField(null=True, blank=True)
    imagem = models.ImageField(null=True, blank=True)
    status = models.BooleanField(default=True)

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome
    


class Produto(models.Model):
    nome = models.CharField(max_length=100, null=False, blank=False)
    descricao = models.TextField(null=True, blank=True)
    imagem = models.ImageField(null=True, blank=True)
    valor = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.BooleanField(default=True)

    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name="produtos")

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome
