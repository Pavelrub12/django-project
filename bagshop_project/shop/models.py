from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(verbose_name="Описание", blank=True)

    def __str__(self):
        return self.name

class Manufacturer(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    country = models.CharField(max_length=100, verbose_name="Страна")
    description = models.TextField(verbose_name="Описание", blank=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(verbose_name="Описание", blank=True)
    product_img = models.ImageField(verbose_name="Фото товара", upload_to="products/", blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена", validators=[MinValueValidator(0)])
    quantity = models.IntegerField(verbose_name="Количество на складе", validators=[MinValueValidator(0)])
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, verbose_name="Производитель")

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart", verbose_name="Пользователь")
    create_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f'Корзина пользователя {self.user.username}'

    def total_price(self):
        total = sum(item.element_price() for item in self.items.all())
        return total

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items", verbose_name="Корзина")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="cart_items", verbose_name="Товар")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Число товаров", validators=[MinValueValidator(1)])

    def __str__(self):
        return f"{self.product.name} ({self.quantity} шт.)"

    def element_price(self):
        return self.product.price * self.quantity

    def clean(self):
        if self.quantity > self.product.quantity:
            raise ValidationError(f'Недостаточно товара на складе. Доступно: {self.product.quantity}')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата заказа")
    address = models.TextField(verbose_name="Адрес доставки")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Итого")
    
    def __str__(self):
        return f"Заказ #{self.id} - {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items", verbose_name="Заказ")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    quantity = models.PositiveIntegerField(verbose_name="Количество")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    
    def __str__(self):
        return f"{self.product.name} x{self.quantity}"
    
class Profile(models.Model):
    """Профиль пользователя"""
    
    ROLE_CHOICES = [
        ('CUSTOMER', 'Покупатель'),
        ('ADMIN', 'Администратор'),
        ('MANAGER', 'Менеджер'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=200, verbose_name="Полное имя", blank=True)
    phone = models.CharField(max_length=20, verbose_name="Телефон", blank=True)
    address = models.TextField(verbose_name="Адрес доставки", blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='CUSTOMER', verbose_name="Роль")
    
    favorite_category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Любимая категория")
    city = models.CharField(max_length=100, verbose_name="Город", blank=True)
    postal_code = models.CharField(max_length=20, verbose_name="Индекс", blank=True)
    
    def __str__(self):
        return f"Профиль {self.user.username}"
    
    def is_admin(self):
        return self.role == 'ADMIN' or self.user.is_superuser

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()