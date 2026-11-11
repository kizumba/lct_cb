import logging
from decimal import Decimal

from django.db.models import Sum
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import ItemAdicional, ItemPedido, Pedido

logger = logging.getLogger(__name__)


def recalcular_subtotal_pedido(pedido_id):
    """Recalcula valor_subtotal do Pedido a partir dos itens.

    Não mexe em valor_total: deixa o save() do Pedido cuidar disso
    (valor_subtotal + taxa_entrega - desconto).
    """
    try:
        pedido = Pedido.objects.get(pk=pedido_id)
    except Pedido.DoesNotExist:
        return

    total = (
        ItemPedido.objects.filter(pedido_id=pedido_id)
        .aggregate(s=Sum("preco_total"))["s"]
        or Decimal("0.00")
    )

    if pedido.valor_subtotal != total:
        pedido.valor_subtotal = total
        # Não use update_fields=['valor_total'] aqui:
        # queremos que o save() do Pedido recalcule valor_total.
        pedido.save(update_fields=["valor_subtotal", "valor_total", "atualizado_em"])



@receiver([post_save, post_delete], sender=ItemPedido)
def atualizar_total_por_item(sender, instance, **kwargs):
    logger.info("Signal ItemPedido disparado: pk=%s", instance.pk)
    recalcular_subtotal_pedido(instance.pedido_id)


@receiver([post_save, post_delete], sender=ItemAdicional)
def atualizar_total_por_adicional(sender, instance, **kwargs):
    logger.info("Signal ItemAdicional disparado: pk=%s", instance.pk)
    # Guarda contra cascade delete: item_pedido pode não existir mais
    try:
        pedido_id = instance.item_pedido.pedido_id
    except (ItemPedido.DoesNotExist, AttributeError):
        return
    recalcular_subtotal_pedido(pedido_id)