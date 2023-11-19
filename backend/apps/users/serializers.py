from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model
from django.db import transaction

from .models import ProfileModel, UserModel as User

UserModel: User = get_user_model()


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = ProfileModel
        fields = ('id', 'name', 'surname')


class UserSerializer(ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = UserModel
        fields = ('id', 'email', 'password', 'is_active', 'is_staff',
                  'is_superuser', 'created_at', 'updated_at', 'total_reading_time_7_days', 'total_reading_time_30_days',
                  'profile')

        read_only_fields = ('id', 'is_active', 'is_staff',
                            'is_superuser', 'created_at', 'updated_at', 'total_reading_time_7_days',
                            'total_reading_time_30_days')

        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    @transaction.atomic
    def create(self, validated_data):
        profile = validated_data.pop('profile')
        user = UserModel.objects.create_user(**validated_data)
        ProfileModel.objects.create(**profile, user=user)
        return user
