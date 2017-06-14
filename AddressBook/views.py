from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)

from AddressBook.models import AddressBook
from AddressBook.permissions import IsAuthenticatedAndOwnerPermission
from AddressBook.serializers import AddressBookSerializer


class AddressBookViewMixin(object):
    model = AddressBook
    permission_classes = (IsAuthenticatedAndOwnerPermission,)
    serializer_class = AddressBookSerializer

    def get_queryset(self):
        """Get objects only for currently logged in user"""
        return self.model.objects.filter(owner=self.request.user)


class AddressBookList(AddressBookViewMixin, ListCreateAPIView):
    """List all entries of address book or create a new one.
    Filtering by url parameters."""
    filter_backends = (DjangoFilterBackend,)
    filter_fields = (
        'address',
        'email',
        'mobile_number',
        'name_and_surname',
    )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class AddressBookDetails(AddressBookViewMixin, RetrieveUpdateDestroyAPIView):
    """Return entry of address book to be modified/deleted."""
