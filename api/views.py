from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView

from common.pagination import StandardPagination
from common.utils import ok, created
from .models import Post, UserPostLike
from .serializers import PostSerializer, PostLikeValueSerializer, PostInfoSerializer


class CreateListApiView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    pagination_class = StandardPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetailApiView(APIView):

    def get(self, request, pk):
        post = get_object_or_404(Post, id=pk)
        seri_post = PostInfoSerializer(post, context={'user': request.user}).data
        return ok(seri_post)

    def post(self, request, pk):
        post = get_object_or_404(Post, id=pk)
        try:
            like_rel = UserPostLike.objects.get(user=request.user, post_id=pk)
            serializer = PostLikeValueSerializer(instance=like_rel, data=request.data)
        except UserPostLike.DoesNotExist:
            serializer = PostLikeValueSerializer(data=request.data)
        serializer.context['post'] = post
        serializer.context['user'] = request.user
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return created(serializer.data)


# class LikeAnalytics(APIView):
#
#     def get(self, request):
#         self.request.query_params
