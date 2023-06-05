from typing import Callable
import pytest
from django.urls import reverse
from rest_framework import status


@pytest.fixture()
def contacts_create_data(faker) -> Callable:
    def _wrapper(**kwargs) -> dict:
        data = {'email': faker.email()}
        data |= kwargs
        return data

    return _wrapper


class TestContactsView:
    url = reverse('contacts-list')

    def test_auth_required(self, client, contacts_create_data):
        """Не авторизованный пользователь при создании контактных данных получит ошибку авторизации"""

        response = client.post(self.url, data=contacts_create_data())
        assert response.status_code == status.HTTP_403_FORBIDDEN
