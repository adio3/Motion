from django.db import IntegrityError
from django.db.models import Q
from django.http import Http404
from rest_framework.generics import GenericAPIView, ListAPIView, ListCreateAPIView, RetrieveAPIView
from rest_framework.response import Response

from rest_framework import filters, status

from friend_request.models import FriendRequest
from .models import User
from .serializers import UserProfileSerializerPrivate, UserProfileSerializerPublic, FriendRequestDetails, \
    FriendsSerializer


class ListUserProfileInfo(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializerPrivate

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = queryset.get(pk=self.request.user.id)
        # here you can check for object permissions
        return obj

    def get(self, request, *args, **kwargs):
        return Response(self.get_serializer(request.user).data)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ListAllUsers(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializerPublic
    search_fields = ["first_name", "last_name", "username"]
    filter_backends = (filters.SearchFilter,)


"""
    def get(self, request, *args, **kwargs):
        search = request.query_params.get('search');
        if search:
            result = self.get_queryset().filter(first_name__icontains=search)
            serializer = self.get_serializer(result, many=True)
            return Response(serializer.data)
        else:
            result = self.get_queryset()
            serializer = self.get_serializer(result, many=True)
            return Response(serializer.data)
"""


class RetrieveUserProfile(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializerPublic
    lookup_url_kwarg = "user_id"
    lookup_field = "id"

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class ToggleFollowUserView(GenericAPIView):
    serializer_class = UserProfileSerializerPrivate
    queryset = User.objects.all()
    lookup_url_kwarg = "user_id"
    lookup_field = "id"

    def post(self, request, *args, **kwargs):
        current_user = request.user
        user_to_be_followed = self.get_object()
        if user_to_be_followed != current_user:
            if user_to_be_followed in current_user.followees.all():
                current_user.followees.remove(user_to_be_followed)
            else:
                current_user.followees.add(user_to_be_followed)

        return Response(self.get_serializer(current_user).data)


class ListFollowers(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializerPublic

    def get_queryset(self):
        return self.request.user.followers

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ListFollowees(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializerPublic

    def get_queryset(self):
        return self.request.user.followees

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class SendFriendRequest(GenericAPIView):
    serializer_class = UserProfileSerializerPrivate
    queryset = User.objects.all()
    lookup_url_kwarg = "user_id"
    lookup_field = "id"

    def post(self, request, *args, **kwargs):
        sender = request.user
        receiver = self.get_object()
        try:
            if (receiver in sender.friends_with.all() or receiver in sender.friends_of.all()):
                return Response(data={"error": "You are already friend with this user."}, status=500)
            elif sender.received_friend_requests.filter(sender=receiver):
                return Response(data={"error": "You have a pending friend request from this user."}, status=500)
            elif sender == receiver:
                return Response(data={"error": "You cannot send a friend request to yourself."}, status=500)
            else:
                new_friend_request = Friend_request(sender=sender, receiver=receiver, status="pending")
                new_friend_request.save()

        except IntegrityError as e:
            print("Duplicate friend request error: ")
            return Response(data={"error": "Friend request already exists."}, status=500)

        return Response(self.get_serializer(sender).data)


class ListUpdateDeleteFriendRequest(GenericAPIView):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestDetails
    lookup_url_kwarg = "friend_request_id"
    lookup_field = "id"

    def delete(self, request, *args, **kwargs):
        try:
            friend_request_to_be_deleted = self.get_object()
            friend_request_to_be_deleted.delete()
        except Http404:
            return Response(data={"error": "no such friend request"}, status=404)

        return Response(data={"success": "Friend request has been deleted."}, status=200)

    def get(self, request, *args, **kwargs):
        try:
            FriendRequest = self.get_object()

        except Http404:
            return Response(data={"error": "no such friend request"}, status=404)

        return Response(self.get_serializer(FriendRequest).data)

    def patch(self, request, *args, **kwargs):

        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            if (request.data["status"] == "accepted"):
                # not added twice if already there.. so working fine, but why? :)
                request.user.friends_with.add(instance.sender)
            elif (request.data["status"] == "rejected"):
                instance.delete()

        except Http404:
            return Response(data={"error": "no such friend request"}, status=404)

        return Response(serializer.data)


class ListAllFriends(GenericAPIView):
    serializer_class = FriendsSerializer
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        filtered_queryset = self.get_queryset().filter(
            Q(friends_with=self.request.user) | Q(friends_of=self.request.user))
        serializer = self.get_serializer(filtered_queryset, many=True)
        return Response(serializer.data)
