from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Posts, Comment

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = ['user', 'content', 'created_at']

class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    # like_count = serializers.IntegerField(source='like_count', read_only=True)
    user = serializers.StringRelatedField()

    class Meta:
        model = Posts
        fields = ['id', 'user', 'content', 'image', 'likers', 'created_at', 'comments']


class CommentPostSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'post', 'content', 'created_at']
