from rest_framework.serializers import (
    CharField, IntegerField, ModelSerializer, Serializer, ValidationError,
)

from goods.models import Category, Good, ShoppingCart, Subcategory


class NumberSerializer(Serializer):
    """Сериализатор проверки валидности данных для create_noms_row."""

    number = IntegerField()

    def validate_number(self, value):
        """
        Валидация для поля 'number'.
        """
        if value < 1:
            raise ValidationError(
                "Поле 'number' должно быть целым положительным числом."
            )
        return value

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


class SubcategoryGetShortSerializer(ModelSerializer):
    """
    Сериализатор представления объектов Subcategory в усеченном виде.
    Используется для отображения названия, цены и категории товара
    в ShoppingCartGetSerializer.."""

    parent_category = CharField(source='category.name')

    class Meta:
        model = Subcategory
        fields = (
            'id',
            'name',
            'slug',
            'parent_category',
        )


class GoodGetSerializer(ModelSerializer):
    """Сериализатор представления объектов Good."""

    subcategory = SubcategoryGetShortSerializer()

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


class GoodGetShortSerializer(ModelSerializer):
    """
    Сериализатор представления объектов Good в усеченном виде.
    Используется для отображения названия, цены и категории товара
    в ShoppingCartGetSerializer.
    """

    subcategory = SubcategoryGetSerializer()

    class Meta:
        model = Good
        fields = (
            'id',
            'name',
            'price',
            'subcategory',
        )


class ShoppingCartGetSerializer(ModelSerializer):
    """
    Сериализатор представления объектов ShoppingCart.
    """

    good = CharField(source='good.name')
    price = IntegerField(source='good.price')

    class Meta:
        model = ShoppingCart
        fields = (
            'good',
            'price',
            'amount',
        )


class ShoppingCartShortSerializer(ModelSerializer):
    """
    Сериализатор представления объектов ShoppingCart в усеченном виде.
    Используется для валидации названия и количества товара
    в ShoppingCartPostListSerializer.
    """

    class Meta:
        model = ShoppingCart
        fields = (
            'good',
            'amount',
        )


class ShoppingCartPostListSerializer(ModelSerializer):
    """Сериализатор добавления списка объектов ShoppingCart."""

    goods = ShoppingCartShortSerializer(many=True)

    class Meta:
        model = ShoppingCart
        fields = (
            'user',
            'goods',
        )

    def validate(self, attrs):
        goods = attrs.get('goods')
        if not goods:
            raise ValidationError(
                {
                    "goods": [
                        {
                            "good": [
                                "Обязательное поле."
                            ],
                            "amount": [
                                "Обязательное поле."
                            ]
                        }
                    ]
                }
            )
        goods_names: list[str] = []
        for good in goods:
            goods_names.append(good['good'])
        goods_set = set(goods_names)
        if len(goods) != len(goods_set):
            raise ValidationError(
                {
                    "goods": [
                        {
                            "good": [
                                "Значение поля должно быть уникальным."
                            ]
                        }
                    ]
                }
            )
        return super().validate(attrs)

    def create(self, validated_data):
        shopping_items: list[ShoppingCart] = []
        for item in validated_data['goods']:
            shopping_items.append(
                ShoppingCart(
                    user=validated_data['user'],
                    good=item['good'],
                    amount=item['amount'],
                )
            )
        objects: list[ShoppingCart] = (
            ShoppingCart.objects.bulk_create(shopping_items)
        )
        self.context['objects'] = objects
        return objects

    def to_representation(self, instance):
        objects: list[ShoppingCart] = self.context['objects']
        total_goods = len(objects)
        total_sum = sum(
            object.good.price * object.amount for object in objects
        )
        goods: list[dict[str, any]] = []
        for object in objects:
            goods.append(
                {
                    'good': object.good.name,
                    'price': object.good.price,
                    'amount': object.amount,
                }
            )
        data = {
            'total_goods': total_goods,
            'total_sum': total_sum,
            'goods': goods,
        }
        return data
