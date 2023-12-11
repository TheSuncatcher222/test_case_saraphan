# Тестовое задание для "Сарафан" (backend)

Реализовать проект магазина продуктов со следующим функционалом:
 - категории товаров
❌ Должна быть реализована возможность создания, редактирования, удаления категорий и подкатегорий товаров в Django Admin.
❌ Категории и подкатегории обязательно должны иметь "наименование", "slug-имя", "изображение".
❌ Подкатегории должны быть связаны с родительской категорией.
❌ Должен быть реализован эндпоинт для просмотра всех категорий с подкатегориями. Должна быть предусмотрена пагинация.
 - товары
❌ Должна быть реализована возможность создания, редактирования, удаления продуктов в Django Admin.
❌ Продукты должны относится к определенной категории и подкатегории.
❌ Продукты должны иметь наименование, slug-имя, изображение в 3-х размерах, цену.
❌ Должен быть реализован эндпоинт для просмотра всех продуктов. Должна быть предусмотрена пагинация.
 - корзина товаров
❌ Реализовать эндпоинт добавления, изменения (изменение количества), удаления продукта в корзине.
❌ Реализовать эндпоинт вывода состава корзины с подсчетом количества товаров и суммы стоимости товаров в корзине.
❌ Реализовать возможность полной очистки корзины.
 - права доступа
❌ Операции по эндпоинтам категорий и продуктов может осуществлять любой пользователь
❌ Операции по эндпоинтам корзины может осуществлять только авторизированный пользователь и только со своей корзиной
❌ Реализовать авторизацию по токену.