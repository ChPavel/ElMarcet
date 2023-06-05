from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from network.models import Provider, Product, Contacts, User


class ProviderSerializer(serializers.ModelSerializer):
    """Сериализатор поставщика для всех действий кроме создания и изменения"""

    user: User = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Provider
        fields = '__all__'
        read_only_fields = ('lev',)


class ForPutProviderSerializer(ProviderSerializer):
    """Сериализатор поставщика для его изменения"""

    class Meta:
        model = Provider
        fields = '__all__'
        read_only_fields = ('credit', 'lev')


class CreateProviderSerializer(ProviderSerializer):
    """Сериализатор поставщика для его создания"""

    def create(self, validated_data: dict) -> Provider:
        """Метод автоматически определяет уровень объекта в сети и указывает в поле 'type_provider' значение 'Factory'
        в случае не заполнения поля 'type_provider'. Предположено, что завод, будучи нижним уровнем в сети продажи
        электроники, не может иметь поставщика электроники т.к. производит её, а имеет поставщиков комплектующих,
        находящихся за пределами сети продажи электроники."""
        self_provider: Provider = validated_data.get('self_provider')

        if not self_provider:
            validated_data.update({'lev': 0, 'type_provider': 'Factory'})
            return super().create(validated_data)

        elif self_provider.lev == 2:
            raise ValidationError(
                'Поставщик товаров с lev=2 не может являться поставщиком для новых участников сети, выберите поставщика с уровнем 0 или 1'
            )

        else:
            self_provider.lev += 1
            validated_data.update({'lev': self_provider.lev})
            return super().create(validated_data)


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор продукции"""

    user: User = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Product
        fields = '__all__'


class ContactsSerializer(serializers.ModelSerializer):
    """Сериализатор контактных данных"""

    user: User = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Contacts
        fields = '__all__'
