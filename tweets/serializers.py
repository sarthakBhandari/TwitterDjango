from rest_framework import serializers
from .models import Tweet
from django.conf import settings
from profiles.serializers import PublicProfileSerializer
TWEET_ACTION_OPTIONS = settings.TWEET_ACTION_OPTIONS



class TweetActionSerializer(serializers.Serializer):
    #recieving data(id, and action) from xhr send request
    id = serializers.IntegerField()
    action = serializers.CharField()

    def validate_action(self, value):
        value = value.lower().strip()
        if value not in TWEET_ACTION_OPTIONS:
            raise serializers.ValidationError("not a valid action for tweets")
        return value

class TweetCreateSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only=True)
    user = PublicProfileSerializer(source='user.profile', read_only=True)

    class Meta:
        model = Tweet
        fields = ['user', 'id', 'content', 'likes', 'timestamp']
    
    def get_likes(self, obj):
        return obj.likes.count()

    def validate_content(self, value):
        if len(value) > 240:
            raise serializers.ValidationError('tweet is too long')
        return value


class TweetSerializer(serializers.ModelSerializer):
    user = PublicProfileSerializer(source='user.profile', read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)
    parent = TweetCreateSerializer(read_only=True)
    class Meta:
        model = Tweet
        fields = ['user', 'id', 'content', 'likes', 'is_retweet', 'parent', 'timestamp']
    
    def get_likes(self, obj):
        return obj.likes.count()

    def validate_content(self, value):
        if len(value) > 240:
            raise serializers.ValidationError('tweet is too long')
        return value
    
        