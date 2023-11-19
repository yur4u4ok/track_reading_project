from django.db import models
from django.contrib.auth import get_user_model

from apps.users.models import UserModel as User

UserModel: User = get_user_model()


class BookModel(models.Model):
    class Meta:
        db_table = 'books'

    name = models.CharField(max_length=30)
    author = models.CharField(max_length=30)
    year = models.IntegerField()
    short_description = models.CharField(max_length=128)
    full_description = models.TextField()

    def __str__(self):
        return self.name


class BooksUsersReadModel(models.Model):
    class Meta:
        db_table = 'books_users'

    start_reading = models.DateTimeField(null=True)
    end_reading = models.DateTimeField(null=True)
    book = models.ForeignKey(BookModel, on_delete=models.CASCADE, related_name='book_read')
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='user_read')
