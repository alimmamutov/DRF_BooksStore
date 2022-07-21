from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Book(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=17, decimal_places=2)
    author_name = models.CharField(max_length=255)

    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, default=None, related_name='my_books')
    '''
    Назначив related_name='my_books, мы дали возможность обращаться ко всем книгам , 
    где Юзер - владелец, через модель юзера
    Пример:
    user = User.objects.get(id=2)
    user.my_books.all()
    '''

    readers = models.ManyToManyField(User, through='UserBookRelation', related_name='books') # Здесь прочитанными будут
    # считаться книги которые присвоены юзеру в таблице UserBookRelation - сделали это с помощью
    # through='UserBookRelation'
    '''
    Назначив related_name='books, мы дали возможность обращаться ко всем книгам , 
    где Юзер - читал книги(те, которые указаны в UserBookRelations - through='UserBookRelation'), через модель юзера
    Пример:
    user = User.objects.get(id=2)
    user.my_books.all()
    '''
    def __str__(self):
        return f'{self.name}'


class UserBookRelation(models.Model):
    RATE_CHOICES = (
        (1, 'Ok'),
        (2, 'Fine'),
        (3, 'Good'),
        (4, 'Amazing'),
        (5, 'Incredible'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    in_bookmarks = models.BooleanField(default=False)
    rate = models.PositiveSmallIntegerField(choices=RATE_CHOICES, null=True)

    def __str__(self):
        return f'{self.book.name} <-> {self.user.username}'