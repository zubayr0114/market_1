from datetime import timedelta

from ckeditor.fields import RichTextField
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import JSONField, IntegerField, PositiveIntegerField, DecimalField, Model, CharField, SET_NULL, \
    ForeignKey, TextChoices, TextField, BooleanField, SlugField
from django.utils.text import slugify
from django.utils.timezone import now
from django_resized import ResizedImageField
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def created_at_product(self):
        return self.created_at.strftime('%d-%m-%Y')


class User(AbstractUser):
    class Type(TextChoices):
        ADMIN = "admin", "Admin"
        CURRIER = "currier", "Yetkazib beruvchi"
        USERS = "users", "Foydalanuvchi"
        OPERATOR = "operator", "Operator"
        MANAGER = "manager", "Manajer"

    type = CharField(max_length=25, choices=Type.choices, default=Type.USERS)
    intro = models.TextField(max_length=1024, blank=True)
    avatar = ResizedImageField(size=[168, 168], upload_to='user_avatars/', null=True, blank=True,
                               default='user_avatars/avatar_default.jpeg')
    banner = ResizedImageField(size=[1198, 124], upload_to='user_banners/', null=True, blank=True,
                               default='user_avatars/banner_default.jpg')
    workout = CharField(max_length=50)
    country = CharField(max_length=30)
    is_verified = BooleanField(default=False)
    phone_number = models.CharField(max_length=20)


class Category(MPTTModel):
    name = models.CharField(max_length=30)
    slug = SlugField(max_length=25, null=True, blank=True, unique=True)
    parent = TreeForeignKey('self', SET_NULL, 'category', null=True, blank=True)
    image = ResizedImageField(size=[100, 100], upload_to='category_images/', null=True, blank=True,
                              default='user_avatars/banner_default.jpg')

    class Meta:
        verbose_name = 'Kategoriya'
        verbose_name_plural = 'Kategoriyalar'


    def __str__(self):
        return self.name

    def _get_unique_slug(self):
        slug = slugify(self.name)
        unique_slug = slug
        num = 1
        while Product.objects.filter(slug=unique_slug).exists():
            unique_slug = f'{slug}-{num}'
            num += 1
        return unique_slug

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = self._get_unique_slug()
        if force_update is True:
            self.slug = slugify(self.name)
        return super().save(force_insert, force_update, using, update_fields)


class WishList(models.Model):
    user = ForeignKey('apps.User', on_delete=models.CASCADE, related_name='wishlists')
    product = ForeignKey('apps.Product', on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)


class Product(BaseModel):
    name = CharField(max_length=255)
    price = DecimalField(max_digits=9, decimal_places=2)
    description = RichTextField()
    specifications = JSONField(null=True, blank=True)
    discount = IntegerField(default=0)
    quantity = PositiveIntegerField(default=0)
    shipping = DecimalField(max_digits=12, decimal_places=2, default=0)
    slug = SlugField(max_length=25, null=True, blank=True, unique=True)
    category = models.ForeignKey('apps.Category', models.CASCADE, 'categories')

    class Meta:
        verbose_name = 'Mahsulot'
        verbose_name_plural = 'Mahsulotlar'

    @property
    def stock(self):
        if self.quantity > 0:
            return "Sotuvda bor"
        else:
            return "Sotuvda yoq"

    @property
    def sale_price(self):
        return self.price * self.discount / 100

    @property
    def sell_price(self):
        return self.price - self.sale_price

    @property
    def is_new(self):
        return self.created_at >= now() - timedelta(days=2)

    def _get_unique_slug(self):
        slug = slugify(self.name)
        unique_slug = slug
        num = 1
        while Product.objects.filter(slug=unique_slug).exists():
            unique_slug = f'{slug}-{num}'
            num += 1
        return unique_slug

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.slug = self._get_unique_slug()
        if force_update is True:
            self.slug = slugify(self.name)
        return super().save(force_insert, force_update, using, update_fields)


class ProductImage(Model):
    image = ResizedImageField(size=[1098, 717], upload_to='product_images/', null=True, blank=True)
    product = models.ForeignKey('apps.Product', models.CASCADE, related_name='images')


class Order(Model):
    name = CharField(max_length=25)
    phone_number = models.CharField(max_length=20)
    quantity = PositiveIntegerField(default=1)
    product = models.ForeignKey('apps.Product', models.CASCADE)

    @property
    def total_price(self):
        return self.quantity * self.product.price


class SiteSettings(Model):
    delivery_price = DecimalField(max_digits=12, decimal_places=2, )
