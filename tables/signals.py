from .models import Order, PaymentStatus
from django.db.models.signals import post_save, post_delete, pre_save
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
        else:
            table = instance.table
            table.is_occupied = True
            table.save()


@receiver(post_delete, sender=Order)
def clear_table_after_order_delete(sender, instance, **kwargs):
    if instance:
        table = instance.table
        table.is_occupied = False
        table.save()


@receiver(pre_save, sender=Order)
def handle_table_change(sender, instance, **kwargs):
    """Make old table available if order is moved to a new table."""
    if instance.pk:
        print(instance.pk)  # Check if this is an update
        try:
            old_instance = Order.objects.get(pk=instance.pk)
            print(old_instance, "hello")
            if old_instance.table != instance.table:
                old_table = old_instance.table
                old_table.is_occupied = False
                old_table.save()
        except Order.DoesNotExist:
            pass  # If order does not ex
