from django.urls import path

from .views import ListCreateBooksView, GetBookView, StartReadingSessionView, EndReadingSessionView, \
    GetEveryBookReadingTimeView, GetGeneralTimeView

urlpatterns = [
    path('', ListCreateBooksView.as_view(), name='list_create_books'),
    path('/<int:pk>', GetBookView.as_view(), name='retrieve_book'),
    path('/<int:pk>/start_session', StartReadingSessionView.as_view(), name='start_reading_session'),
    path('/<int:pk>/end_session', EndReadingSessionView.as_view(), name='end_reading_session'),
    path('/every_book_time', GetEveryBookReadingTimeView.as_view(), name='get_every_book_reading_time'),
    path('/general_time', GetGeneralTimeView.as_view(), name='get_general_reading_time'),
]
