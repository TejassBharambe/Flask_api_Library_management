

import unittest
import requests

BASE_URL = 'http://127.0.0.1:5000'


class LibraryManagementSystemTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Login and get token for tests."""
        url = f"{BASE_URL}/login"
        payload = {
            'username': 'admin',
            'password': 'password'
        }
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            raise Exception(f"Login failed: {response.status_code} - {response.text}")
        cls.token = response.json().get('token')
        cls.headers = {'x-access-token': cls.token}
        cls.book_id = None
        cls.member_id = None

    def create_book_and_get_id(self):
        """Create a book and return its ID."""
        if not self.__class__.book_id:
            url = f"{BASE_URL}/books"
            payload = {
                'title': 'The Great Gatsby',
                'author': 'F. Scott Fitzgerald',
                'year': 1925
            }
            response = requests.post(url, headers=self.headers, json=payload)
            self.assertEqual(response.status_code, 201)
            self.__class__.book_id = response.json()['book']['id']
        return self.__class__.book_id

    def create_member_and_get_id(self):
        """Create a member and return their ID."""
        if not self.__class__.member_id:
            url = f"{BASE_URL}/members"
            payload = {
                'name': 'xyz',
                'email': 'xyz@example.com'
            }
            response = requests.post(url, headers=self.headers, json=payload)
            self.assertEqual(response.status_code, 201)
            self.__class__.member_id = response.json()['member']['id']
        return self.__class__.member_id

    def test_01_login(self):
        """Test login functionality."""
        url = f"{BASE_URL}/login"
        payload = {
            'username': 'admin',
            'password': 'password'
        }
        response = requests.post(url, json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.json())

    def test_02_add_book(self):
        """Test adding a book."""
        book_id = self.create_book_and_get_id()
        self.assertIsNotNone(book_id)

    def test_03_get_books(self):
        """Test retrieving all books."""
        url = f"{BASE_URL}/books"
        response = requests.get(url, headers=self.headers)
        self.assertEqual(response.status_code, 200)

    def test_04_search_books(self):
        """Test searching books by title."""
        self.create_book_and_get_id()  
        url = f"{BASE_URL}/books"
        params = {'title': 'The Great Gatsby'}
        response = requests.get(url, headers=self.headers, params=params)
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.json().get('books', [])), 0)

    def test_05_get_single_book(self):
        """Test retrieving a single book."""
        book_id = self.create_book_and_get_id()
        url = f"{BASE_URL}/books/{book_id}"
        response = requests.get(url, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('book', {}).get('id'), book_id)

    def test_06_update_book(self):
        """Test updating a book."""
        book_id = self.create_book_and_get_id()
        url = f"{BASE_URL}/books/{book_id}"
        payload = {'year': 1930}
        response = requests.put(url, headers=self.headers, json=payload)
        self.assertEqual(response.status_code, 200)

    def test_07_delete_book(self):
        """Test deleting a book."""
        book_id = self.create_book_and_get_id()
        url = f"{BASE_URL}/books/{book_id}"
        response = requests.delete(url, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.__class__.book_id = None  # Reset book ID

    def test_08_add_member(self):
        """Test adding a member."""
        member_id = self.create_member_and_get_id()
        self.assertIsNotNone(member_id)

    def test_09_get_members(self):
        """Test retrieving all members."""
        url = f"{BASE_URL}/members"
        response = requests.get(url, headers=self.headers)
        self.assertEqual(response.status_code, 200)

    def test_10_get_single_member(self):
        """Test retrieving a single member."""
        member_id = self.create_member_and_get_id()
        url = f"{BASE_URL}/members/{member_id}"
        response = requests.get(url, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get('member', {}).get('id'), member_id)

    def test_11_update_member(self):
        """Test updating a member."""
        member_id = self.create_member_and_get_id()
        url = f"{BASE_URL}/members/{member_id}"
        payload = {'email': 'newemail@example.com'}
        response = requests.put(url, headers=self.headers, json=payload)
        self.assertEqual(response.status_code, 200)

    def test_12_delete_member(self):
        """Test deleting a member."""
        member_id = self.create_member_and_get_id()
        url = f"{BASE_URL}/members/{member_id}"
        response = requests.delete(url, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.__class__.member_id = None  # Reset member ID


if __name__ == '__main__':
    unittest.main()
