from django.db import models


class OrderStatus(models.TextChoices):
    PENDING = "Pending", "Pending"
    COMPLETED = "Completed", "Completed"


class PaymentStatus(models.TextChoices):
    PENDING = "Pending", "Pending"
    PAID = "Paid", "Paid"


class Tables(models.Model):
    number = models.IntegerField(unique=True)
    is_occupied = models.BooleanField(default=False)

    def __str__(self):
        return (
            f"Table {self.number} ({'Occupied' if self.is_occupied else 'Available'})"
        )


class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Menu(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.ImageField(upload_to="menu_images", null=True, blank=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    table = models.ForeignKey(Tables, on_delete=models.CASCADE)
    menu = models.ManyToManyField(Menu)
    quantity = models.IntegerField()
    status = models.CharField(
        max_length=100, choices=OrderStatus.choices, default=OrderStatus.PENDING
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    @property
    def total_amount(self):
        return self.menu.price * self.quantity


class Billing(models.Model):
    table = models.ForeignKey(Tables, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=100, choices=PaymentStatus.choices, default=PaymentStatus.PENDING
    )
    timestamp = models.DateTimeField(auto_now_add=True)


"""class OrderList(models.CharField):
    table=models.ManyToManyField(Tables)
    order=models.ForeignKey(Order, on_delete=models.CASCADE,related_name="orders")
    quantity=models.IntegerField()
    total_amount=models.IntegerField() """
