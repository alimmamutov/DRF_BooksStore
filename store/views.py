# from django.shortcuts import render

# Create your views here.
from django.db.models import Count, Case, When
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from store.models import Book, UserBookRelation
from store.permissions import IsOwnerOrStaffOrReadOnly
from store.serializers import BooksSerializer, UserBookRelationSerializer


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all().annotate(
            annotatated_likes=Count(Case(When(userbookrelation__like=True, then=1))))
    serializer_class = BooksSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    permission_classes = [IsOwnerOrStaffOrReadOnly]
    filter_fields = ('price',)
    search_fields = ('name', 'author_name',)
    ordering_fields =('name', 'price', 'id',)

    def perform_create(self, serializer): # Это дополнение к методу create (чтробы не переопределять сам метод create)
        serializer.validated_data['owner'] = self.request.user
        serializer.save()


class UserBookRelationViewSet(UpdateModelMixin,
                       GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = UserBookRelation.objects.all()
    serializer_class = UserBookRelationSerializer
    lookup_field = 'book' # Эта настройка говорит о том, что в запрос будет ждать атрибут 'book' в юрл
    # ^api/book_relation/(?P<book>[^/.]+)/$ [name='userbookrelation-detail']

    '''
        Переназначили метод получения таким образом:
            -   Если такой связи нет (связка книга и юзер), 
        то она создается. 
            -   Если связь есть , то изменяется
    '''
    def get_object(self):
        obj, created = UserBookRelation.objects.get_or_create(user=self.request.user,
                                                        book_id=self.kwargs['book'])
        print('created', created)
        return obj


def auth(request):
    return render(request, 'oauth.html')