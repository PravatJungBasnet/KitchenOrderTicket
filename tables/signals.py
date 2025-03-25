from .models import Order, PaymentStatus
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=Order)
def update_table_status(sender, instance, created, **kwargs):
    if created:
        if instance.payment_status == PaymentStatus.PENDING:
            table = instance.table
            table.is_occupied = True
            table.save()


@receiver(post_save, sender=Order)
def clear_table_status(sender, instance, created, **kwargs):
    if not created:
        if instance.payment_status == PaymentStatus.PAID:
            table = instance.table
            table.is_occupied = False
            table.save()
