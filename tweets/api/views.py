from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from ..models import Tweet
import random
from ..forms import TweetForm
from django.utils.http import is_safe_url
from django.conf import settings
from ..serializers import TweetSerializer, TweetActionSerializer, TweetCreateSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

# Create your views here.
def home_view_notanymore(request, *args, **kwargs):
    # return HttpResponse("<h1>Home page</h1>")
    return render(request, "pages/feed.html")

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def tweet_create_view(request, *args, **kwargs):
    serializer = TweetCreateSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)
    return Response({}, status=400)

def get_paginated_query_set_response(qs, request):
    paginator = PageNumberPagination()
    paginator.page_size = 20
    paginator_qs = paginator.paginate_queryset(qs, request)
    serializer = TweetSerializer(paginator_qs, many=True, context={"request":request})
    return paginator.get_paginated_response(serializer.data) #Response(serializer.data, 200)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def tweet_feed_view(request, *args, **kwargs):
    qs = Tweet.objects.feed(request.user)
    return get_paginated_query_set_response(qs, request) #Response(serializer.data, 200)

@api_view(["GET"])
def tweet_api_list_view(request, *args, **kwargs):
    qs = Tweet.objects.all()
    username = request.GET.get("username")
    if username != None:
        qs = qs.by_username(username)
    # serializer = TweetSerializer(qs, many=True)
    # return Response(serializer.data)
    return get_paginated_query_set_response(qs, request)

@api_view(["GET"])
def tweet_api_detail_view(request, tweet_id, *args, **kwargs):
    qs = Tweet.objects.filter(id=tweet_id)
    if not qs.exists():
        return Response({}, status=404)
    obj = qs.first() #first match from the query set
    serializer = TweetSerializer(obj)
    return Response(serializer.data, status=200)

@api_view(['DELETE','POST'])
@permission_classes([IsAuthenticated])
def tweet_delete_view(request, tweet_id, *args, **kwargs):
    qs = Tweet.objects.filter(id=tweet_id) #tweet exits
    if not qs.exists():
        return Response({}, status=404)
    qs = qs.filter(user=request.user) #tweet for the user thats logged in
    if not qs.exists():
        return Response({"message":"permission not allowed"}, status=401)
    obj = qs.first() #first match from the query set
    obj.delete()
    return Response({"message":"Tweet successfully removed"}, status=204)


@api_view(['POST']) #Post -> some data is being sent with the request
@permission_classes([IsAuthenticated])
def tweet_action_view(request, *args, **kwargs):
    serializer = TweetActionSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        tweet_id = data.get("id")
        tweet_action = data.get("action")
        qs = Tweet.objects.filter(id=tweet_id)
        print(tweet_id)
        if not qs.exists():
            return Response({}, status=404)
        obj = qs.first()
        if tweet_action == "like":
            obj.likes.add(request.user)
            serializer = TweetSerializer(obj)
            return Response(serializer.data, status=200)
        elif tweet_action == "unlike":
            obj.likes.remove(request.user)
            serializer = TweetSerializer(obj)
            return Response(serializer.data, status=200)
        elif tweet_action == "retweet":
            new_tweet = Tweet.objects.create(parent=obj, user=request.user, content=obj.content)
            serializer = TweetSerializer(new_tweet)
            return Response(serializer.data, status=201)
    return Response({}, status=200)


    

def tweet_create_view_pure_django(request, *args, **kwargs):
    user = request.user
    if not request.user.is_authenticated:
        user = None
        if request.is_ajax():
            return JsonResponse({}, status=401)
        return redirect(settings.LOGIN_URL)

    form = TweetForm(request.POST or None)
    next_url = request.POST.get("next") or None #next is a hidden input field in the home form
    #print("next url is ",next_url, "finish")
    
    if form.is_valid():
        obj = form.save(commit=False)
        #do other form related logic
        obj.user = user
        obj.save()
        if request.is_ajax():
            return JsonResponse(obj.serialize(),status=201) #201 created successfully
        #redirect after saving the form
        if next_url and is_safe_url(next_url, allowed_hosts=settings.ALLOWED_HOSTS):
            return redirect(next_url)
        form = TweetForm()
    if form.errors:
        if request.is_ajax():
            return JsonResponse(form.errors, status=400)
    return render(request, "components/form.html", context={"form":form})

def tweet_list_view_pure_django(request, *args, **kwargs):
    qs = Tweet.objects.all()
    tweet_list = [x.serialize() for x in qs]
    data = {
        "response": tweet_list
    }
    return JsonResponse(data=data)

