from django.contrib.auth.models import User
from rest_framework.test import (
    APIClient,
    APITestCase
)

AB_FIRST_ENTRY = {
    'address': 'foo-bar 39, 166',
    'id': 1,
    'email': 'fff@ff.pl',
    'mobile_number': 888555888,
    'name_and_surname': 'ff ff'
}

ADDRESS_BOOK_URL = '/api/address_book/'
DETAILS_FIRST_URL = ADDRESS_BOOK_URL + 'details/1/'


class AddressBookForLoggedInUserTest(APITestCase):
    """Test cases for logged in user"""

    def setUp(self):
        self.api_client = APIClient()
        self.username = 'foo'
        self.email = 'foo@foo.foo'
        self.password = 'password'
        User.objects.create_user(self.username, self.email, self.password)
        User.objects.create_user('hdoan', self.email, self.password)
        self.api_client.login(username=self.username, password=self.password)

    def tearDown(self):
        self.api_client.logout()

    def _create_entry(self):
        return self.api_client.post(ADDRESS_BOOK_URL, data={
            'address': 'foo-bar 39, 166',
            'email': 'fff@ff.pl',
            'mobile_number': 888555888,
            'name_and_surname': 'ff ff'
        })

    def test_address_book(self):
        """Create new address book"""
        response = self.api_client.get(ADDRESS_BOOK_URL)
        self.assertEqual(response.status_code, 200)

        response = self._create_entry()
        self.assertEqual(response.status_code, 201)

        response = self.api_client.get(ADDRESS_BOOK_URL)
        self.assertEqual(response.json()[0], AB_FIRST_ENTRY)

        # Login to different user
        self.api_client.logout()
        self.api_client.login(username='hdoan', password=self.password)
        response = self.api_client.get(ADDRESS_BOOK_URL)
        self.assertEqual(response.json(), [])

    def test_put(self):
        """Modify entry of address book"""
        self._create_entry()
        #  Get details of created address book
        response = self.api_client.get(DETAILS_FIRST_URL)
        self.assertEqual(response.json(), AB_FIRST_ENTRY)

        # Modify entry
        expected_put = {
            'address': 'updated 39, 166',
            'email': 'updated_email@ff.pl',
            'id': 1,
            'mobile_number': 123555888,
            'name_and_surname': 'updated_name updated_surname'
        }
        response = self.api_client.put(DETAILS_FIRST_URL, data=expected_put)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected_put)

    def test_delete(self):
        """Delete entry of address book"""
        self._create_entry()

        response = self.api_client.get(DETAILS_FIRST_URL)
        self.assertEqual(response.json(), AB_FIRST_ENTRY)
        response = self.api_client.delete(DETAILS_FIRST_URL,
                                          data=AB_FIRST_ENTRY)
        self.assertEqual(response.status_code, 204)

        response = self.api_client.get(DETAILS_FIRST_URL)
        self.assertEqual(response.status_code, 404)

    def test_create_empty_entry_validation(self):
        response = self.api_client.post(ADDRESS_BOOK_URL, data={
            'address': None,
            'email': None,
            'mobile_number': None,
            'name_and_surname': ''
        })
        self.assertDictEqual(response.data, {
            'address': ['This field may not be null.'],
            'email': ['This field may not be null.'],
            'mobile_number': ['This field may not be null.'],
            'name_and_surname': ['This field may not be blank.']
        })

    def test_filter(self):
        """Basic filtering by url parameters"""
        self._create_entry()
        self.api_client.post(ADDRESS_BOOK_URL, data={
            'address': '0-bar 39, 166',
            'email': '0@ff.pl',
            'mobile_number': 111111111,
            'name_and_surname': '0 ff'
        })
        self.api_client.post(ADDRESS_BOOK_URL, data={
            'address': '1-bar 39, 166',
            'email': '1@ff.pl',
            'mobile_number': 888555888,
            'name_and_surname': '1 ff'
        })
        response = self.api_client.get(ADDRESS_BOOK_URL +
                                       '?email=0@ff.pl')
        self.assertEqual(1, len(response.json()))

        response = self.api_client.get(ADDRESS_BOOK_URL +
                                       '?mobile_number=888555888')
        self.assertEqual(2, len(response.json()))

        response = self.api_client.get(ADDRESS_BOOK_URL +
                                       '?address=sunshine street')
        self.assertEqual(0, len(response.json()))
