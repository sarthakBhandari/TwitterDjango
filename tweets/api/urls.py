from django.urls import path
from .views import (tweet_api_detail_view, tweet_api_list_view, 
tweet_create_view, tweet_delete_view, tweet_action_view,
tweet_feed_view) 

urlpatterns = [
    path('create-tweet', tweet_create_view),
    path('api/tweets/<int:tweet_id>/', tweet_api_detail_view),
    path('api/tweets/', tweet_api_list_view),
    path('api/tweets/create/', tweet_create_view),
    path('api/tweets/<int:tweet_id>/delete/', tweet_delete_view),
    path('api/tweets/action/',tweet_action_view),
    path('api/tweets/feed/', tweet_feed_view)
]