from django.contrib import admin
from .models import *


# Register your models here.

class BookAdmin(admin.ModelAdmin):
    # fields = ('name', 'price')
    # readonly_fields = ('id', )
    # fields = tuple((f.name for f in Book._meta.get_fields() if not f.is_relation))
    # aaa = tuple((f.name for f in Book._meta.get_fields()))
    list_display = ('id', 'name', 'price', 'author_name', 'owner')


@admin.register(UserBookRelation)
class UserBookRelation(admin.ModelAdmin):
    # readonly_fields = ('id',)
    # fields = ('id', 'book', 'user', 'like', 'in_bookmarks' ,'rate',)
    list_display = ('id', 'book', 'user', 'like', 'in_bookmarks' ,'rate')
    pass


admin.site.register(Book, BookAdmin)
