from django.test import TestCase
from .models import Tweet
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
User = get_user_model()

# Create your tests here.
class TweetTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="abc", password="123") #create_user NOT create
        Tweet.objects.create(content="abc", user=self.user) #set up data gets stored in the alias database
        Tweet.objects.create(content="123", user=self.user)
        Tweet.objects.create(content="098", user=self.user)


    def test_tweet_created(self): #test_ is needed
        tweet_obj = Tweet.objects.create(content="abc", user=self.user)
        self.assertEqual(tweet_obj.id, 4)
        self.assertEqual(tweet_obj.user, self.user)
    
    def get_client(self):
        client = APIClient()
        client.login(username=self.user.username, password="123")
        return client

    def test_action_like_unlike(self):
        client = self.get_client()
        response = client.post("/api/tweets/action/", 
            {"id": 1, "action": "like"})
        self.assertEqual(response.status_code, 200)
        response = client.post("/api/tweets/action/", {"id":2, "action":"unlike"})
        self.assertEqual(response.status_code, 200)
        like_count = response.json().get("likes")
        self.assertEqual(like_count, 0)
        my_like_instance_count = self.user.tweetlike_set.count()
        self.assertEqual(my_like_instance_count, 1)
        my_related_like = self.user.tweet_user.count()
        self.assertEqual(my_like_instance_count, my_related_like)


    def test_action_retweet(self):
        client = self.get_client()
        response = client.post("/api/tweets/action/", {"id":2, "action":"retweet"})
        self.assertEqual(response.status_code, 201)
        new_tweet_id = response.json().get("id")
        self.assertNotEqual(2, new_tweet_id)
    
    def test_detail_view(self):
        client = self.get_client()
        response = client.get("/api/tweets/3/")
        self.assertEqual(response.status_code, 200)
        _id = response.json().get("id")
        self.assertEqual(3,_id)
    
    def test_tweet_delete(self):
        client = self.get_client()
        response = client.delete("/api/tweets/3/delete/")
        self.assertEqual(response.status_code, 200)
        response = client.delete("/api/tweets/3/delete/")
        self.assertEqual(response.status_code, 404)