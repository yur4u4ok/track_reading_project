from datetime import timedelta
from django.contrib.auth import get_user_model
from django.utils import timezone

from apps.users.models import UserModel as User
from .models import BooksUsersReadModel
from configs.celery import app

from core.time_operations.calculate_time import calculate_time

UserModel: User = get_user_model()


@app.task
def update_reading_statistics():
    users = UserModel.objects.all()

    for user in users:
        seven_days_ago = timezone.now() - timedelta(days=7)
        thirty_days_ago = timezone.now() - timedelta(days=30)

        total_time_7_days = get_total_reading_time(user, seven_days_ago)

        total_time_30_days = get_total_reading_time(user, thirty_days_ago)

        user.total_reading_time_7_days = calculate_time(total_time_7_days)
        user.total_reading_time_30_days = calculate_time(total_time_30_days)
        user.save()


def get_total_reading_time(user, start_date):
    sessions = BooksUsersReadModel.objects.filter(user=user, start_reading__gte=start_date)

    total_time = timedelta()
    for session in sessions:
        if session.end_reading:
            total_time += session.end_reading - session.start_reading
        else:
            total_time += timezone.now() - session.start_reading

    return total_time.total_seconds()
