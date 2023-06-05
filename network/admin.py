from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from network.models import *


admin.site.unregister(Group)
admin.site.site_header = 'Панель администратора торговой сети по продаже электроники'


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Настройка вкладки сотрудников в админпанели."""

    list_display = ['username', 'first_name', 'last_name', 'is_active']
    ordering = ('username',)
    list_filter = ['is_active', 'is_superuser']
    readonly_fields = ('last_login', 'date_joined')
    fieldsets = (
        (None, {'fields': ('password', 'username')}),
        ('Персональная информация', {'fields': ('first_name', 'last_name', 'email', 'role', 'sex')}),
        ('Разрешения', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Настройка вкладки товаров в админ панели"""

    list_display = ('title', 'slug', 'model', 'release')
    ordering = ('title',)
    search_fields = ('title', 'slug', 'model', 'release')
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        ('С продуктом работает', {'fields': ('user',)}),
        ('Сведения о продукте', {'fields': ('title', 'slug', 'model', 'release')}),
    )


@admin.register(Contacts)
class ContactsAdmin(admin.ModelAdmin):
    """Настройка вкладки контактной информации поставщиков в админ панели"""

    list_display = ('country', 'city', 'email', 'street', 'house_number')
    ordering = ('country',)
    search_fields = ('country', 'city', 'email', 'street')
    list_filter = ('country',)
    fieldsets = (
        ('Данные внёс:', {'fields': ('user',)}),
        ('Контактные данные:', {'fields': ('email', 'country', 'city', 'street', 'house_number')}),
    )


@admin.action(description='Обнулить кредиторскую задолженность')
def reset_credit(modeladmin, request, queryset):
    """Метод создания действия администратора по обнулению кредиторской задолженности"""
    queryset.update(credit=0)


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    """Настройка вкладки поставщиков в админ панели"""

    list_display = ('title', 'slug', 'type_provider', 'lev', 'contacts', 'self_provider', 'credit', 'user')
    ordering = ('title',)
    list_display_links = ('title', 'self_provider')
    search_fields = ('title', 'slug', 'self_provider')
    list_filter = ('type_provider', 'contacts__city')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('time_create', 'time_update')
    fieldsets = (
        ('С поставщиком работает:', {'fields': ('user', 'time_create', 'time_update')}),
        ('Сведения о поставщике:', {'fields': ('title', 'slug', 'type_provider', 'lev', 'contacts')}),
        ('Ассортимент', {'fields': ('products',)}),
        ('Партнёр', {'fields': ('self_provider', 'credit')}),
    )
    actions = [reset_credit]
