from django import forms
from .models import Produto, Categoria

class ProdutoModelForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'descricao', 'valor', 'categoria', 'imagem']


class CategoriaModelForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome', 'descricao', 'imagem', 'status']