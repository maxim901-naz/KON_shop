from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Item(models.Model):
    name=models.CharField(max_length=50)
    price=models.DecimalField(max_digits=10, decimal_places=2)
    stock=models.PositiveIntegerField(default="Нет в наличии.")
    image = models.ImageField(upload_to='images/')
    info = models.TextField(default="Описание скоро появится.")

    def __str__(self):
        return self.name
class Cart(models.Model):
    session_key = models.CharField(max_length=40, null=True, blank=True)  # Для гостей 

    def total_price(self):
        """Общая сумма корзины"""
        return sum(item.total_price() for item in self.items.all())

    def str(self):
        return f"Корзина {self.session_key}" 

class CartItem(models.Model):
    """Товары в корзине"""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        """Общая стоимость товара"""
        return self.quantity * self.item.price

    def str(self):
        return f"{self.item.name} ({self.quantity} шт.)"