from rest_framework import serializers

from auth_.serializers import UserSerializer
from .models import Post, UserPostLike, Analytics


class PostSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    content = serializers.CharField(required=True)
    author = UserSerializer(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'content', 'author', 'created_at', 'likes')


class PostInfoSerializer(PostSerializer):
    value = serializers.SerializerMethodField()

    class Meta(PostSerializer.Meta):
        fields = PostSerializer.Meta.fields + ('value',)

    def get_value(self, obj):
        try:
            value = UserPostLike.objects.get(post_id=obj.id, user=self.context['user']).value
        except UserPostLike.DoesNotExist:
            value = 0
        return value


class PostLikeValueSerializer(serializers.ModelSerializer):
    value = serializers.IntegerField(required=True, write_only=True)
    content = serializers.CharField(read_only=True)
    author = UserSerializer(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'content', 'author', 'created_at', 'likes', 'value')

    def validate_value(self, val):
        if val != 1 and val != -1 and val != 0:
            raise serializers.ValidationError('value must be 1,-1 or 0')
        return val

    def create(self, validated_data):
        user = self.context['user']
        post = self.context['post']
        UserPostLike.objects.create(user=user, post_id=post.id, value=validated_data['value'])
        post.likes += validated_data['value']
        post.save()
        return post

    def update(self, instance, validated_data):
        post = self.context['post']
        val = validated_data['value']
        if instance.value != val:
            post.likes += (val - instance.value)
            post.save()
            instance.value = val
            instance.save()
        return post


class AnalyticsSerializer(serializers.Serializer):
    date_from = serializers.DateField(write_only=True, required=True)
    date_to = serializers.DateField(write_only=True, required=True)
    likes = serializers.IntegerField(read_only=True)
    dislikes = serializers.IntegerField(read_only=True)

    def validate(self, data):
        if data['date_from'] > data['date_to']:
            raise serializers.ValidationError({'date': 'date_from must be before date_to'})
        return data

    def create(self, validated_data):
        filtered = UserPostLike.objects.filter(updated_at__gte=validated_data['date_from'],
                                               updated_at__lte=validated_data['date_to']).exclude(value=0)
        likes = filtered.filter(value=1).count()
        dislikes = filtered.filter(value=-1).count()
        return Analytics(likes, dislikes)

    def update(self, instance, validated_data):
        pass
