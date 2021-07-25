from django.urls import path
from .views import profile_api_view, api_feed_view

"""
BASE END POINT IS
'/api/profiles/'
"""

urlpatterns = [
    path('<str:username>/feed/', api_feed_view),
    path("<str:username>/follow", profile_api_view),
    path('<str:username>/', profile_api_view),
]
