from django.test import TestCase

from store.models import Book
from store.serializers import BooksSerializer


class BookSerializerTestCase(TestCase):
    def test_ok(self):
        book_1 = Book.objects.create(name='Test book 1', price=25, author_name='Bill Knowledge')
        book_2 = Book.objects.create(name='Test book 2', price=45, author_name='Kim Chang')
        data = BooksSerializer([book_1,book_2],many=True).data
        expected_data = [
            {
                'id': book_1.id,
                'name': 'Test book 1',
                'price': '25.00',
                'author_name': 'Bill Knowledge',
            },
            {
                'id': book_2.id,
                'name': 'Test book 2',
                'price': '45.00',
                'author_name': 'Kim Chang',
            },
        ]
        self.assertEqual(expected_data, data)
