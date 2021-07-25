from rest_framework import serializers
from .models import Profile

class PublicProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.SerializerMethodField(read_only=True)
    last_name = serializers.SerializerMethodField(read_only=True)
    username = serializers.SerializerMethodField(read_only=True)
    following_count = serializers.SerializerMethodField(read_only=True)
    followers_count = serializers.SerializerMethodField(read_only=True)
    is_following = serializers.SerializerMethodField(read_only=True)


    class Meta:
        model =Profile
        fields = ['first_name', 'last_name','id',
            'bio','location','timestamp', 'followers_count', 'following_count', 'username', 'is_following'] 
    
    def get_is_following(self, obj):
        context = self.context
        request = context.get("request", None)
        is_following = False
        if request:
            user = request.user
            is_following = user in obj.followers.all()
        return is_following

    def get_first_name(self, obj):
        return obj.user.first_name

    def get_last_name(self, obj):
        return obj.user.last_name

    def get_username(self, obj):
        return obj.user.username

    def get_following_count(self, obj):
        return obj.user.following.count() #following is related name of followers field
    
    def get_followers_count(self, obj):
        return obj.followers.count()
