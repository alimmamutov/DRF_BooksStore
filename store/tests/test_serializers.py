from django.contrib.auth.models import User
from django.db.models import Count, Case, When, Avg
from django.test import TestCase

from store.models import Book, UserBookRelation
from store.serializers import BooksSerializer


class BookSerializerTestCase(TestCase):
    def setUp(self): # Эта функция будет вызываться перед каждым тестом

        self.user1 = User.objects.create(username='test_user_1', )
        self.user2 = User.objects.create(username='test_user_2', )
        self.user3 = User.objects.create(username='test_user_3', )

        self.book_1 = Book.objects.create(name='Test book 1', price=25, author_name='Bill Knowledge')
        self.book_2 = Book.objects.create(name='Test book 2', price=45, author_name='Kim Chang')

        self.book_rel_1 = UserBookRelation.objects.create(user=self.user1, book=self.book_1, like=True, rate=2)
        self.book_rel_2 = UserBookRelation.objects.create(user=self.user2, book=self.book_1, like=True, rate=1)
        self.book_rel_3 = UserBookRelation.objects.create(user=self.user3, book=self.book_1, like=True, rate=5)

        self.book_rel_1 = UserBookRelation.objects.create(user=self.user1, book=self.book_2, like=True, )
        self.book_rel_2 = UserBookRelation.objects.create(user=self.user2, book=self.book_2, like=True, )
        self.book_rel_3 = UserBookRelation.objects.create(user=self.user3, book=self.book_2, like=False,)

    def test_ok(self):
        books = Book.objects.all().annotate(
            annotatated_likes=Count(Case(When(userbookrelation__like=True, then=1))),
            rating=Avg('userbookrelation__rate')
        ).order_by('id')
        # data = BooksSerializer([self.book_1, self.book_2],many=True).data
        data = BooksSerializer(books,many=True).data
        expected_data = [
            {
                'id': self.book_1.id,
                'name': 'Test book 1',
                'price': '25.00',
                'author_name': 'Bill Knowledge',
                'likes_count': 3,
                'annotatated_likes': 3,
                'rating': '2.67',
            },
            {
                'id': self.book_2.id,
                'name': 'Test book 2',
                'price': '45.00',
                'author_name': 'Kim Chang',
                'likes_count': 2,
                'annotatated_likes': 2,
                'rating': None,
            },
        ]
        self.assertEqual(expected_data, data)
