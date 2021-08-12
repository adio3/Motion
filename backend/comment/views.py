from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response
from .models import Comment
from .serializers import CommentSerializer

from post.models import Post


class ListCreateComments(GenericAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_url_kwarg = "post_id"
    lookup_field = 'post'

    def post(self, request, post_id, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user, post=Post.objects.get(pk=post_id))
        return Response(serializer.data)

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)