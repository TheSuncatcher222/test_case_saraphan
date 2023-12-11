from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models

from backend.settings import (
    CATEGORY_NAME_MAX_LEN, CATEGORY_SLUG_MAX_LEN,
    SHOPPING_CART_MIN_AMOUNT,
    SUBCATEGORY_NAME_MAX_LEN, SUBCATEGORY_SLUG_MAX_LEN,
    set_category_image_name,
    set_good_image_l_name, set_good_image_m_name, set_good_image_s_name,
    set_subcategory_image_name,
)


class Category(models.Model):
    """Модель категорий товаров."""

    name = models.CharField(
        verbose_name='Наименование',
        max_length=CATEGORY_NAME_MAX_LEN,
        unique=True,
    )
    slug = models.SlugField(
        verbose_name='URL',
        max_length=CATEGORY_SLUG_MAX_LEN,
        unique=True,
    )
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to=set_category_image_name,
        # TODO: удалить blank и null при релизе.
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория товаров'
        verbose_name_plural = 'Категории товаров'

    def __str__(self):
        return f'{self.name}'


class Subcategory(models.Model):
    """Модель подкатегорий товаров."""

    name = models.CharField(
        verbose_name='Наименование',
        max_length=SUBCATEGORY_NAME_MAX_LEN,
        unique=True,
    )
    slug = models.SlugField(
        verbose_name='URL',
        max_length=SUBCATEGORY_SLUG_MAX_LEN,
        unique=True,
    )
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to=set_subcategory_image_name,
        # TODO: удалить blank и null при релизе.
        blank=True,
        null=True,
    )
    category = models.ForeignKey(
        verbose_name='Категория',
        to=Category,
        related_name='subcategory',
        on_delete=models.PROTECT,
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Подкатегория товаров'
        verbose_name_plural = 'Подкатегории товаров'

    def __str__(self):
        return f'{self.name} ({self.category.name})'


class Good(models.Model):
    """Модель товаров."""

    name = models.CharField(
        verbose_name='Наименование',
        max_length=SUBCATEGORY_NAME_MAX_LEN,
        unique=True,
    )
    slug = models.SlugField(
        verbose_name='URL',
        max_length=SUBCATEGORY_SLUG_MAX_LEN,
        unique=True,
    )
    price = models.PositiveIntegerField(
        verbose_name='Цена товара',
    )
    subcategory = models.ForeignKey(
        verbose_name='Подкатегория',
        to=Subcategory,
        related_name='good',
        on_delete=models.PROTECT,
    )
    image_large = models.ImageField(
        verbose_name='Изображение (L)',
        upload_to=set_good_image_l_name,
        # TODO: удалить blank и null при релизе.
        blank=True,
        null=True,
    )
    image_medium = models.ImageField(
        verbose_name='Изображение (M)',
        upload_to=set_good_image_m_name,
        # TODO: удалить blank и null при релизе.
        blank=True,
        null=True,
    )
    image_small = models.ImageField(
        verbose_name='Изображение (S)',
        upload_to=set_good_image_s_name,
        # TODO: удалить blank и null при релизе.
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return f'{self.name} ({self.price})'


class ShoppingCart(models.Model):
    """
    Модель товаров в корзине.

    Many-to-Many таблица, связывает пользователей User и товары Good.
    """

    user = models.ForeignKey(
        verbose_name='Пользователь',
        to=User,
        related_name='shopping_cart',
        on_delete=models.CASCADE,
    )
    good = models.ForeignKey(
        verbose_name='Товар',
        to=Good,
        related_name='shopping_cart',
        on_delete=models.CASCADE,
    )
    amount = models.PositiveIntegerField(
        verbose_name='Количество',
        validators=[
            MinValueValidator(
                limit_value=SHOPPING_CART_MIN_AMOUNT,
                message='Ни одного товара не было добавлено в корзину!',
            ),
        ],
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'good',),
                name='unique_user_good',
            ),
        ]
        ordering = ('id',)
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзинах'

    def __str__(self):
        return f'{self.user}: {self.good.name} ({self.amount})'
