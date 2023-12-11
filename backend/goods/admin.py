from django.contrib import admin

from backend.settings import ADMIN_ITEMS_PER_PAGE
from goods.models import Category, Good, ShoppingCart, Subcategory


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Переопределяет административный интерфейс Django для модели Category.

    Атрибуты:
        - list_display (tuple) - список полей для отображения в интерфейсе:
            - ID (id)
            - наименование (name)
            - URL (slug)
            - изображение (image)
        - list_editable (tuple) - список полей для изменения в интерфейсе:
            - наименование (name)
            - URL (slug)
            - изображение (image)
        - search_fields (tuple) - список полей для поиска объектов:
            - наименование (name)
            - URL (slug)
        - list_per_page (int) - количество объектов на одной странице
    """
    list_display = (
        'id',
        'name',
        'slug',
        'image',
    )
    list_editable = (
        'name',
        'slug',
        'image',
    )
    search_fields = (
        'name',
        'slug',
    )
    list_per_page = ADMIN_ITEMS_PER_PAGE


@admin.register(Good)
class GoodAdmin(admin.ModelAdmin):
    """
    Переопределяет административный интерфейс Django для модели Good.

    Атрибуты:
        - list_display (tuple) - список полей для отображения в интерфейсе:
            - ID (id)
            - наименование (name)
            - URL (slug)
            - цена (price)
            - подкатегория (subcategory)
            - изображение (L) (image_large)
            - изображение (M) (image_medium)
            - изображение (S) (image_small)
        - list_editable (tuple) - список полей для изменения в интерфейсе:
            - наименование (name)
            - URL (slug)
            - цена (price)
            - подкатегория (subcategory)
            - изображение (L) (image_large)
            - изображение (M) (image_medium)
            - изображение (S) (image_small)
        - search_fields (tuple) - список полей для поиска объектов:
            - наименование (name)
            - URL (slug)
            - цена (price)
        - list_filter (tuple) - список фильтров:
            - подкатегория (subcategory)
        - list_per_page (int) - количество объектов на одной странице
    """
    list_display = (
        'id',
        'name',
        'slug',
        'price',
        'subcategory',
        'image_large',
        'image_medium',
        'image_small',
    )
    list_editable = (
        'name',
        'slug',
        'price',
        'subcategory',
        'image_large',
        'image_medium',
        'image_small',
    )
    search_fields = (
        'name',
        'slug',
        'price',
    )
    list_filter = (
        'subcategory',
    )
    list_per_page = ADMIN_ITEMS_PER_PAGE


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    """
    Переопределяет административный интерфейс Django для модели ShoppingCart.

    Атрибуты:
        - list_display (tuple) - список полей для отображения в интерфейсе:
            - ID (id)
            - пользователь (user)
            - товар (good)
            - количество (amount)
        - list_editable (tuple) - список полей для изменения в интерфейсе:
            - пользователь (user)
            - товар (good)
            - количество (amount)
        - list_filter (tuple) - список фильтров:
            - пользователь (user)
            - товар (good)
        - list_per_page (int) - количество объектов на одной странице
    """
    list_display = (
        'id',
        'user',
        'good',
        'amount',
    )
    list_editable = (
        'user',
        'good',
        'amount',
    )
    list_filter = (
        'user',
        'good',
    )
    list_per_page = ADMIN_ITEMS_PER_PAGE


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    """
    Переопределяет административный интерфейс Django для модели Subcategory.

    Атрибуты:
        - list_display (tuple) - список полей для отображения в интерфейсе:
            - ID (id)
            - наименование (name)
            - URL (slug)
            - изображение (image)
            - категория (category)
        - list_editable (tuple) - список полей для изменения в интерфейсе:
            - наименование (name)
            - URL (slug)
            - изображение (image)
            - категория (category)
        - search_fields (tuple) - список полей для поиска объектов:
            - наименование (name)
            - URL (slug)
        - list_filter (tuple) - список фильтров:
            - категория (category)
        - list_per_page (int) - количество объектов на одной странице
    """
    list_display = (
        'id',
        'name',
        'slug',
        'image',
        'category',
    )
    list_editable = (
        'name',
        'slug',
        'image',
        'category',
    )
    search_fields = (
        'name',
        'slug',
    )
    list_filter = (
        'category',
    )
    list_per_page = ADMIN_ITEMS_PER_PAGE
