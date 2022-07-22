from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from store.models import Book, UserBookRelation


class BooksSerializer(ModelSerializer):

    # Реализация подсчета лайков через доп метод
    likes_count = serializers.SerializerMethodField() # Такое поле будет искать функцию get_<имя поля>

    # Реализация подсчета лайков через annotate (В самом вью вызываем  books = Book.objects.all().annotate(
    # annotatated_likes=<Формула подсчета>) он прибавит к каждой строчке бвыборки колонку annotated_like
    annotatated_likes = serializers.IntegerField(read_only=True) # Ставим только чтение для того, чтобы было не
    # обязательно указывать это поле при отправке запроса

    rating = serializers.DecimalField(max_digits=3, decimal_places=2)

    class Meta:
        model = Book
        fields = ('id', 'name', 'price', 'author_name', 'likes_count', 'annotatated_likes', 'rating')
        # fields = ('id', 'name')

    def get_likes_count(self, instance): # Эта функция используется для SerializerMethodField поля likes_count
        return UserBookRelation.objects.filter(book=instance, like=True).count()

class UserBookRelationSerializer(ModelSerializer):
    class Meta:
        model = UserBookRelation
        fields = ('book','like','in_bookmarks','rate',)
