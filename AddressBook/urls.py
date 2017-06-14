from django.conf.urls import url, include

from AddressBook.views import (
    AddressBookList,
    AddressBookDetails,
)

urlpatterns = [
    url(r'^address_book/', include([
        url(r'^$', AddressBookList.as_view()),
        url(r'^details/(?P<pk>[0-9]+)/$', AddressBookDetails.as_view()),
    ]))
]
