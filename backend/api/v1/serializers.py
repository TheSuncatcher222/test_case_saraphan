from rest_framework.serializers import ModelSerializer

from goods.models import Category, Good, ShoppingCart, Subcategory


class CategoryGetSerializer(ModelSerializer):
    """Сериализатор представления объектов Category."""

    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'slug',
            'image',
        )


class SubcategoryGetSerializer(ModelSerializer):
    """Сериализатор представления объектов Subcategory."""

    category = CategoryGetSerializer()

    class Meta:
        model = Subcategory
        fields = (
            'id',
            'name',
            'slug',
            'category',
            'image',
        )


class GoodGetSerializer(ModelSerializer):
    """Сериализатор представления объектов Good."""

    subcategory = SubcategoryGetSerializer()

    class Meta:
        model = Good
        fields = (
            'id',
            'name',
            'slug',
            'price',
            'subcategory',
            'image_large',
            'image_medium',
            'image_small',
        )
