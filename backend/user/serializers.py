from rest_framework import serializers

from friend_request.models import FriendRequest
from .models import User


class UserProfileSerializerPrivate(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class UserProfileSerializerPublic(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'date_joined', 'first_name', 'last_name']


class FriendRequestDetails(serializers.ModelSerializer):

    class Meta:
        model = FriendRequest
        fields = '__all__'


class FriendsSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name']