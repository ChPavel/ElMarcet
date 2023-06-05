from typing import Callable
import pytest
from django.urls import reverse
from rest_framework import status


@pytest.fixture()
def product_create_data(faker) -> Callable:
    def _wrapper(**kwargs) -> dict:
        data = {'title': faker.sentence(7)}
        data |= kwargs
        return data

    return _wrapper


class TestProductView:
    url = reverse('product-list')

    def test_auth_required(self, client, product_create_data):
        """Не авторизованный пользователь при создании товара получит ошибку авторизации"""

        response = client.post(self.url, data=product_create_data())
        assert response.status_code == status.HTTP_403_FORBIDDEN
