from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Produto, Categoria


class ProdutoListView(ListView):
    model = Produto
    template_name = 'produto_list.html'
    context_object_name = 'produtos'

    def get_queryset(self):
        produtos = super().get_queryset().order_by("nome")
        search = self.request.GET.get("search")
        if search:
            produtos = produtos.filter(nome__icontains=search)
        return produtos


class ProdutoCreateView(CreateView):
    model = Produto
    template_name = 'produto_form.html'
    fields = ['nome', 'descricao', 'valor', 'categoria', 'imagem']
    success_url = reverse_lazy('produto_list')

class ProdutoUpdateView(UpdateView):
    model = Produto
    template_name = 'produtos/produto_form.html'
    fields = ['nome', 'descricao', 'valor', 'categoria', 'imagem']
    success_url = reverse_lazy('produto_list')

class ProdutoDeleteView(DeleteView):
    model = Produto
    template_name = 'produtos/produto_confirm_delete.html'
    success_url = reverse_lazy('produto_list')


class CategoriaListView(ListView):
    model = Categoria
    template_name = 'categoria_list.html'
    context_object_name = 'categorias'

class CategoriaCreateView(CreateView):
    model = Categoria
    template_name = 'categoria_form.html'
    fields = ['nome', 'descricao', 'imagem', 'status']
    success_url = reverse_lazy('categoria_list')    