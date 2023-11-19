from rest_framework.serializers import ModelSerializer

from .models import BookModel, BooksUsersReadModel
from apps.users.serializers import UserSerializer


class BookSerializer(ModelSerializer):
    class Meta:
        model = BookModel
        fields = ('id', 'name', 'author', 'year', 'short_description')


class BookFullSerializer(ModelSerializer):
    class Meta:
        model = BookModel
        fields = ('id', 'name', 'author', 'year', 'short_description', 'full_description')


class BooksUsersReadSerializer(ModelSerializer):
    book = BookSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = BooksUsersReadModel
        fields = ('id', 'start_reading', 'end_reading', 'book', 'user')
