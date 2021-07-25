from django.test import TestCase
from .models import Profile
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()

# Create your tests here.
class ProfileTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="abcd", password="123")
        self.userb = User.objects.create_user(username="efg", password="123")
    def test_profile_create_via_signal(self):
        qs = Profile.objects.all()
        self.assertEqual(qs.count(), 2)

    def test_following(self):
        first = self.user
        second = self.userb
        first_pro = self.user.profile
        second_pro = self.userb.profile
        self.assertEqual(first.following.all().count(), 0)
        second_pro.followers.add(first)
        self.assertEqual(first.following.all().count(), 1)
    
    def get_client(self):
        client = APIClient()
        client.login(username=self.user.username, password="123")
        return client

    def test_api_follow_endpoint(self):
        client = self.get_client()
        response = client.post(f"/api/profiles/{self.userb.username}/follow", {"action":"follow"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("count"), 1)
    
    def test_api_unfollow_endpoint(self):
        client = self.get_client()
        client.post(f"/api/profiles/{self.userb.username}/follow", {"action":"follow"})
        response = client.post(f"/api/profiles/{self.userb.username}/follow", {"action":"unfollow"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("count"), 0)

