from rest_framework import serializers
from AddressBook.models import AddressBook


class AddressBookSerializer(serializers.ModelSerializer):

    class Meta:
        model = AddressBook
        exclude = ('owner', )
