from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response
from .models import Post
from .serializers import PostSerializer


class ListCreatePostsView(GenericAPIView):
    queryset = Post.objects.all().order_by('updated').reverse()
    serializer_class = PostSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)
        return Response(serializer.data)

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class SearchPostsView(GenericAPIView):
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        search_key = self.request.query_params.get('keyword')
        queryset = Post.objects.filter(text__contains=search_key).order_by('updated').reverse()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class GetUpdateDeletePostView(GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GetPostsFromFollowingView(ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        user = self.request.user
        post_from_following = [post for post in Post.objects.all().order_by('updated').reverse() if post.author in user.followees.all()]
        return post_from_following


class GetPostsFromFriendsView(ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        user = self.request.user
        post_from_following = [post for post in Post.objects.all().order_by('updated').reverse() if post.author in user.friends_with.all()]
        return post_from_following


class GetPostByUserIdView(GenericAPIView):
    queryset = Post.objects.all().order_by('updated').reverse()
    lookup_url_kwarg = 'user_id'
    lookup_field = 'author'
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ToggleLikeView(GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_url_kwarg = "post_id"

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        user = self.request.user
        isFavourite = user in post.likes.all()
        if isFavourite:
            post.likes.remove(user)
        else:
            post.likes.add(user)
        return Response(self.get_serializer(post).data)


class ListLikedView(GenericAPIView):
    queryset = Post.objects.all().order_by('updated').reverse()
    serializer_class = PostSerializer

    def get(self, request):
        queryset = self.get_queryset().filter(likes=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)