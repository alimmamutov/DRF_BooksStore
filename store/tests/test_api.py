import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase

from store.models import Book, UserBookRelation
from store.serializers import BooksSerializer


class BooksApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_user', )
        self.user2 = User.objects.create(username='test_user_2', )
        self.user3 = User.objects.create(username='test_user_3_staff', is_staff=True)
        # self.client.force_login(self.user)
        self.book_1 = Book.objects.create(name='Test book 1', price=25, author_name='Author 1', owner=self.user)
        # print(self.book_1.owner)
        self.book_2 = Book.objects.create(name='Test book 2', price=45, author_name='Author 2')
        self.book_3 = Book.objects.create(name='Test book 3 Author 1', price=35, author_name='Author 3')

    def test_get_1(self):
        url = reverse('book-list')
        # print(url)
        response = self.client.get(url)
        serializer_data = BooksSerializer([self.book_1, self.book_2, self.book_3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_filter(self):
        url = reverse('book-list')
        # print(url)
        response = self.client.get(url, data={'search': 'Author 1'})
        serializer_data = BooksSerializer([self.book_1, self.book_3], many=True).data
        self.assertEqual(serializer_data, response.data)

    def test_get_ordering(self):
        url = reverse('book-list')
        # print(url)
        response = self.client.get(url, data={'ordering': '-id'})
        serializer_data = BooksSerializer([self.book_3, self.book_2, self.book_1], many=True).data
        self.assertEqual(serializer_data, response.data)

    def test_create(self):
        self.assertEqual(Book.objects.all().count(), 3)
        url = reverse('book-list')
        data = {
            'name': 'Created book',
            'price': 150.50,
            'author_name': 'Author_Creator'
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.post(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(Book.objects.all().count(), 4)
        self.assertEqual(Book.objects.last().owner, self.user)

    def test_update(self):
        url = reverse('book-detail', args=(self.book_1.id,))
        data = {
            'name': self.book_1.name,
            'price': 999,
            'author_name': self.book_1.author_name
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.put(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        # Здесь обновляем объект книги из базы данных
        # self.book_1 = Book.objects.get(id=self.book_1.id)
        self.book_1.refresh_from_db()

        self.assertEqual(999, self.book_1.price)

    def test_update_not_owner(self):
        url = reverse('book-detail', args=(self.book_1.id,))
        data = {
            'name': self.book_1.name,
            'price': 999,
            'author_name': self.book_1.author_name
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user2)
        response = self.client.put(url, data=json_data, content_type='application/json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual(
            {'detail': ErrorDetail(string='You do not have permission to perform this action.', code='permission_denied')}
, response.data)
        print(response.data)
        self.book_1.refresh_from_db()
        self.assertEqual(25, self.book_1.price)

    def test_update_not_owner_but_staff(self):
        url = reverse('book-detail', args=(self.book_1.id,))
        data = {
            'name': self.book_1.name,
            'price': 999,
            'author_name': self.book_1.author_name
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user3)
        response = self.client.put(url, data=json_data, content_type='application/json')
        print(response.status_code)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        print(response.data)
        self.book_1.refresh_from_db()
        self.assertEqual(999, self.book_1.price)

    def test_delete(self):
        self.assertEqual(Book.objects.all().count(), 3)
        url = reverse('book-detail', args=(self.book_1.id,))
        # data = {
        #     'name': self.book_1.name,
        #     'price': 999,
        #     'author_name': self.book_1.author_name
        # }
        # json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.delete(url, content_type='application/json')
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(Book.objects.all().count(), 2)


class BooksRelationApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='test_user', )
        self.user2 = User.objects.create(username='test_user_2', )
        self.book_1 = Book.objects.create(name='Test book 1', price=25, author_name='Author 1', owner=self.user)
        self.book_2 = Book.objects.create(name='Test book 2', price=45, author_name='Author 2')

    def test_like(self):
        url = reverse('userbookrelation-detail', args=(self.book_1.id, ))
        data = {
            'like': True,
        }
        json_data = json.dumps(data)
        self.client.force_login(self.user)
        response = self.client.patch(url, data=json_data,
                                     content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.book_1.refresh_from_db()
        relation = UserBookRelation.objects.get(user=self.user, book = self.book_1)
        self.assertTrue(relation.like)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = {
            'like': False,
        }
        json_data = json.dumps(data)
        response = self.client.patch(url, data=json_data,
                                     content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)