from typing import Callable
import pytest
from django.urls import reverse
from rest_framework import status


@pytest.fixture()
def provider_create_data(faker) -> Callable:
    def _wrapper(**kwargs) -> dict:
        data = {'title': faker.sentence(7)}
        data |= kwargs
        return data

    return _wrapper


class TestProviderView:
    url = reverse('provider-list')

    def test_auth_required(self, client, provider_create_data):
        """Не авторизованный пользователь при создании поставщика получит ошибку авторизации"""

        response = client.post(self.url, data=provider_create_data())
        assert response.status_code == status.HTTP_403_FORBIDDEN
