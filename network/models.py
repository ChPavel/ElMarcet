from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class User(AbstractUser):
    """Модель пользователя"""

    MALE = 'm'
    FEMALE = 'f'
    SEX = [(MALE, 'Мужской'), (FEMALE, 'Женский')]

    ADMIN = 'Администратор'
    EMPLOYEE = 'Сотрудник'
    ROLE = [(ADMIN, ADMIN), (EMPLOYEE, EMPLOYEE)]

    sex = models.CharField(max_length=1, choices=SEX, default=MALE, verbose_name='Пол')
    role = models.CharField(max_length=13, choices=ROLE, default=EMPLOYEE, verbose_name='Роль')

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'


class Product(models.Model):
    """Модель товара"""

    title = models.CharField(max_length=250, verbose_name='Название товара')
    slug = models.SlugField(max_length=250, unique=True, db_index=True, verbose_name='URL')
    model = models.CharField(max_length=250, verbose_name='Модель')
    release = models.DateField(verbose_name='Дата выхода продукта на рынок')
    user = models.ForeignKey('User', on_delete=models.PROTECT, verbose_name='Сотрудник')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Contacts(models.Model):
    """Модель контактных данных поставщика"""

    email = models.EmailField(max_length=100, unique=True, verbose_name='Email')
    country = models.CharField(max_length=100, verbose_name='Страна')
    city = models.CharField(max_length=100, verbose_name='Город')
    street = models.CharField(max_length=100, verbose_name='Улица')
    house_number = models.CharField(max_length=10, verbose_name='Номер дома')
    user = models.ForeignKey('User', on_delete=models.PROTECT, verbose_name='Сотрудник')

    def __str__(self):
        return f'Контакты: {self.country}, {self.city}, {self.street}, {self.house_number}.'

    class Meta:
        verbose_name = 'Данные поставщика'
        verbose_name_plural = 'Контактные данные'


class BaseProvider(models.Model):
    """Абстрактная модель поставщика"""

    FCT = 'Factory'
    RTL = 'Retail'
    INP = 'Individual'
    TYPE_P = [(FCT, 'Завод'), (RTL, 'Розничная сеть'), (INP, 'Индивидуальный предприниматель')]

    title = models.CharField(max_length=250, verbose_name='Название')
    slug = models.SlugField(max_length=250, unique=True, verbose_name='URL')
    type_provider = models.CharField(max_length=10, choices=TYPE_P, db_index=True, verbose_name='Тип поставщика')
    contacts = models.OneToOneField('Contacts', on_delete=models.PROTECT, verbose_name='Контактные данные')
    products = models.ManyToManyField('Product', verbose_name='Товары')
    credit = models.DecimalField(max_digits=14, decimal_places=2, verbose_name='Задолженность кредиторская')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Запись создана')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Запись изменена')
    user = models.ForeignKey('User', on_delete=models.PROTECT, verbose_name='Сотрудник')

    def __str__(self):
        return self.title

    class Meta:
        abstract = True


class Provider(BaseProvider):
    """Модель поставщика"""

    BASE = 0
    FIR = 1
    SEC = 2
    LEV = [(BASE, 0), (FIR, 1), (SEC, 2)]

    self_provider = models.ForeignKey('self', on_delete=models.PROTECT, blank=True, null=True, verbose_name='Поставщик')
    lev = models.PositiveSmallIntegerField(choices=LEV, default=BASE, verbose_name='Уровень в сети')

    def get_absolute_url(self):
        """Метод получения url для каждого поставщика по 'pk'."""
        return reverse('provider-detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщики'
