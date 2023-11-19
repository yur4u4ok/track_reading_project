from datetime import datetime, timedelta
from django.utils import timezone

from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from core.time_operations.calculate_time import calculate_time
from .serializers import BookSerializer, BookFullSerializer, BooksUsersReadSerializer
from .models import BookModel, BooksUsersReadModel


class ListCreateBooksView(ListCreateAPIView):
    """
    Get all books
    """

    queryset = BookModel.objects.all()
    serializer_class = BookSerializer
    permission_classes = (AllowAny,)

    def post(self, *args, **kwargs):
        data = self.request.data

        if data and data['year'] > str(datetime.now().year):
            return Response(f'The year must be {datetime.now().year} or less', status.HTTP_400_BAD_REQUEST)

        serializer = BookFullSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)


class GetBookView(RetrieveAPIView):
    """
    Get book by id
    """

    queryset = BookModel.objects.all()
    serializer_class = BookFullSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, *args, **kwargs):
        book = self.get_object()
        book_serializer = self.serializer_class(book)

        queryset = BooksUsersReadModel.objects.filter(book_id=book.id, user=self.request.user).order_by(
            '-start_reading').first()

        last_time_reading = queryset.start_reading if queryset else ''

        result = {
            **book_serializer.data,
            'last_time_reading': last_time_reading
        }

        return Response(result, status=status.HTTP_200_OK)


class StartReadingSessionView(GenericAPIView):
    """
    Start the reading session
    """

    queryset = BookModel.objects.all()
    serializer_class = BooksUsersReadSerializer

    def post(self, *args, **kwargs):
        book = self.get_object()
        user = self.request.user

        open_reading_session = BooksUsersReadModel.objects.filter(user=user, end_reading=None).last()

        if open_reading_session and open_reading_session.book != book:
            serializer = self.serializer_class(open_reading_session, data={'end_reading': datetime.now()}, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

        current_book_session = BooksUsersReadModel.objects.filter(book=book, user=user).last()

        if current_book_session and not current_book_session.end_reading:
            return Response('You have started a session with this book already.', status.HTTP_400_BAD_REQUEST)

        create_new_session_data = {'start_reading': datetime.now()}

        serializer = self.serializer_class(data=create_new_session_data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user, book=book)

        return Response(serializer.data, status.HTTP_201_CREATED)


class EndReadingSessionView(GenericAPIView):
    """
    End the reading session
    """

    queryset = BookModel.objects.all()
    serializer_class = BooksUsersReadSerializer

    def patch(self, *args, **kwargs):
        book = self.get_object()

        queryset = BooksUsersReadModel.objects.filter(user=self.request.user, book=book).last()

        if queryset.end_reading:
            return Response('Session for this book is closed already.', status.HTTP_400_BAD_REQUEST)

        serializer = BooksUsersReadSerializer(queryset, data={'end_reading': datetime.now()}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status.HTTP_200_OK)


class GetEveryBookReadingTimeView(GenericAPIView):
    """
    Get time by reading every book
    """

    def get_queryset(self):
        return BooksUsersReadModel.objects.filter(user=self.request.user)

    serializer_class = BooksUsersReadSerializer

    def get(self, *args, **kwargs):
        every_book_dict = {}

        for session in self.get_queryset():
            total_time = timedelta()

            if session.end_reading:
                total_time += session.end_reading - session.start_reading
            else:
                total_time += timezone.now() - session.start_reading

            if every_book_dict.get(session.book.name):
                every_book_dict[session.book.name] += total_time.total_seconds()
            else:
                every_book_dict[session.book.name] = total_time.total_seconds()

        every_book_dict = {key: calculate_time(every_book_dict[key]) for key in every_book_dict}

        return Response(every_book_dict, status.HTTP_200_OK)


class GetGeneralTimeView(GenericAPIView):
    """
    Get general time for reading
    """

    def get_queryset(self):
        return BooksUsersReadModel.objects.filter(user=self.request.user)

    def get(self, *args, **kwargs):
        total_time = timedelta()
        for session in self.get_queryset():
            if session.end_reading:
                total_time += session.end_reading - session.start_reading
            else:
                total_time += timezone.now() - session.start_reading

        return Response({'general_time_reading': calculate_time(total_time.total_seconds())}, status.HTTP_200_OK)
