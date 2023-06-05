from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.viewsets import ModelViewSet
from network.models import Product, Contacts, Provider


class IsOwnerOrReadOnly(permissions.IsAuthenticated):
    """Пользовательское разрешение, позволяющее редактировать объект только владельцам."""

    def has_object_permission(self, request: Request, view: ModelViewSet, obj: [Product, Contacts, Provider]) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user
