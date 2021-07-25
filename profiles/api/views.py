from django.contrib.auth import get_user_model
from ..models import Profile
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from profiles.serializers import PublicProfileSerializer
from tweets.serializers import TweetSerializer
from tweets.models import Tweet
from tweets.api.views import get_paginated_query_set_response


User = get_user_model()

# @api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
# def user_follow_view(request, username, *args, **kwargs):
#     me = request.user
#     if me.username == username: #username is the person I want to follow
#         return Response({"count": me.profile.followers.count()}, 200)

#     other_user_qs = User.objects.filter(username=username)
#     if not other_user_qs.exists():
#         return Response({}, 404)
#     other_user = other_user_qs.first()
#     profile_obj = other_user.profile #the profile of the user I want to follow
#     data = request.data or {}

#     action = data.get("action")

#     if action == "follow":
#         profile_obj.followers.add(me)
#     elif action == "unfollow":
#         profile_obj.followers.remove(me)

#     serializer = PublicProfileSerializer(profile_obj, context={"request":request})
#     return Response(serializer.data, 200)

@api_view(['GET', 'POST'])
def profile_api_view(request, username, *args, **kwargs):
    #username is the user I am looking at
    #request.user is me (logged in user)
    qs = Profile.objects.filter(user__username=username)
    if not qs.exists():
        return Response({"detail": "User not found"}, 404)
    profile_obj = qs.first()

    if request.method == "POST":
        if request.user != profile_obj.user:
            me = request.user
            data = request.data or {}
            action = data.get("action")
            if action == "follow":
                profile_obj.followers.add(me)
            elif action == "unfollow":
                profile_obj.followers.remove(me)


    serializer = PublicProfileSerializer(profile_obj, context={"request":request})
    return Response(serializer.data, 200)

@api_view(['GET'])
def api_feed_view(request, username, *args, **kwargs):
    if not request.user.is_authenticated:
        return Response({"detail":"user not authenticated"}, status=403)
    user_qs = User.objects.filter(username=username)
    if not user_qs.exists():
        return Response({"detail":"user not found"}, status=404)
    user = user_qs.first()
    qs = Tweet.objects.feed(user)
    if not qs.exists():
        return Response({"detail":"user has no tweets"}, status=200)
    return get_paginated_query_set_response(qs, request)