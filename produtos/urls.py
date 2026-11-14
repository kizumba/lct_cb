from django.urls import path
from .views import ProdutoListView, ProdutoCreateView, ProdutoUpdateView, ProdutoDeleteView   

urlpatterns = [
    path('produtos/', ProdutoListView.as_view(), name='produto_list'),
    path('produtos/create/', ProdutoCreateView.as_view(), name='produto_create'),
    path('produtos/<int:pk>/update/', ProdutoUpdateView.as_view(), name='produto_update'),
    path('produtos/<int:pk>/delete/', ProdutoDeleteView.as_view(), name='produto_delete'),
]