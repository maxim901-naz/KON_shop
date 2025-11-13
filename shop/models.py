from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(
        max_length=100, 
        verbose_name='Название категории'
    )
    slug = models.SlugField(
        max_length=100, 
        unique=True, 
        verbose_name='URL'
    )
    description = models.TextField(
        blank=True, 
        verbose_name='Описание'
    )
    is_active = models.BooleanField(
        default=True, 
        verbose_name='Активна'
    )
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name='Создана'
    )
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})
# Create your models here.
class Item(models.Model):
    name=models.CharField(max_length=50)
    price=models.DecimalField(max_digits=10, decimal_places=2)
    stock=models.PositiveIntegerField(default="Нет в наличии.")
    image = models.ImageField(upload_to='images/')
    info = models.TextField(default="Описание скоро появится.")

    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name='items',
        verbose_name='Категория',
        null=True,  # Разрешаем null для существующих товаров
        blank=True
    )
    
    # Дополнительные полезные поля
    is_available = models.BooleanField(default=True, verbose_name='Доступен')
    created_at = models.DateTimeField( verbose_name='Создан',default=timezone.now)
    updated_at = models.DateTimeField( verbose_name='Обновлен',default=timezone.now)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        """Обновляем updated_at при сохранении"""
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)
    def get_absolute_url(self):
        return reverse('item_detail', kwargs={'pk': self.pk})
    
    @property
    def stock_status(self):
        """Возвращает статус наличия товара"""
        if self.stock == 0:
            return "Нет в наличии"
        elif self.stock < 5:
            return f"Мало ({self.stock} шт.)"
        else:
            return f"В наличии ({self.stock} шт.)"
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