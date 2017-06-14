from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class AddressBook(models.Model):
    address = models.CharField(max_length=100)
    email = models.EmailField()
    mobile_number = models.IntegerField()
    name_and_surname = models.CharField(max_length=100)
    owner = models.ForeignKey(User, related_name='address_book',
                              editable=False)
