from django.db import models
import random
from django.conf import settings
from django.db.models import Q

User = settings.AUTH_USER_MODEL

# Create your models here.

class TweetLike(models.Model): #this class is just for the timestamp
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey("Tweet", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

#managers for model and queryset
class TweetQuerySet(models.QuerySet):
    def by_username(self, username):
        return self.filter(user__username__iexact=username)
    def feed(self, user):
        # following_profiles = user.following.all() #all the profile objects followed by user
        # followed_user_id = [x.user.id for x in following_profiles] #going through all the values and filtering id
        followed_user_id = []
        if user.following.exists(): #all the profiles that the user follow
            followed_user_id = user.following.values_list("user__id", flat=True) #much more efficient search
        return self.filter(Q(user__id__in=followed_user_id) | Q(user=user)).distinct().order_by("-timestamp")
class TweetManager(models.Manager):
    def get_query_set(self, *args, **kwargs):
        return TweetQuerySet(self.model, using=self._db) 
    def feed(self, user):
        return self.get_query_set().feed(user)

class Tweet(models.Model):
    parent = models.ForeignKey("self", null=True, on_delete=models.SET_NULL)
    #each tweet has one user, if user deleted then all their tweets also deleted
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tweets")
    likes = models.ManyToManyField(User, related_name="tweet_user", blank=True, through=TweetLike)
    content = models.TextField(blank=True, null=True)
    image = models.FileField(upload_to="images/", blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = TweetManager.from_queryset(TweetQuerySet)()

    class Meta:
        ordering = ["-id"]
    
    @property
    def is_retweet(self):
        return self.parent != None
    #was using this when we didnt user restframework serializer 
    # def serialize(self):
    #     return {
    #         "id":self.id,
    #         "content": self.content,
    #         "likes": random.randint(0,200)
    #     }