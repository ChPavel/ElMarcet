from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from network.permissions import IsOwnerOrReadOnly
from network.serializers import *


class ProviderViewSet(ModelViewSet):
    """ViewSet для обработки запросов, связанных с поставщиками"""

    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['contacts__country']

    @action(methods=['get'], detail=False)
    def prod(self, request) -> Response:
        """Метод отображения имеющихся в базе продуктов общим списком"""
        products = Product.objects.all()
        return Response({'Продукты': [p.title for p in products]})

    @action(methods=['get'], detail=False)
    def cont(self, request) -> Response:
        """Метод отображения имеющихся в базе контактных данных поставщиков общим списком"""
        contacts = Contacts.objects.all()
        return Response({'Контакты:': [f'{p.country}, {p.city}, {p.street}, {p.house_number}.' for p in contacts]})

    def get_serializer_class(self):
        """Метод выбора сериализатора в зависимости от поступившего запроса"""
        serializer_class = self.serializer_class

        if self.request.method == 'PUT':
            serializer_class = ForPutProviderSerializer
        elif self.request.method == 'POST':
            serializer_class = CreateProviderSerializer

        return serializer_class


class ContactsViewSet(ModelViewSet):
    """ViewSet для обработки запросов, связанных с контактными данными поставщиков"""

    queryset = Contacts.objects.all()
    serializer_class = ContactsSerializer
    permission_classes = (IsOwnerOrReadOnly,)


class ProductViewSet(ModelViewSet):
    """ViewSet для обработки запросов, связанных с продукцией поставщиков"""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsOwnerOrReadOnly,)
