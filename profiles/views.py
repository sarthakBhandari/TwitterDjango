from django.shortcuts import render, redirect
from .models import Profile
from django.http import Http404
from .forms import ProfileForm
from accounts.views import login_view


def profile_update_view(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("/login?next=/profile/update")
    user = request.user
    my_profile = user.profile #profile -> user are one to one field so allowed
    initial_data={
        "first_name":user.first_name,
        "last_name":user.last_name,
        "email": user.email,
    }
    form = ProfileForm(request.POST or None, instance=my_profile, initial=initial_data)
    if form.is_valid():
        profile_obj = form.save(commit=False)
        first_name = form.cleaned_data.get("first_name")
        last_name = form.cleaned_data.get("last_name")
        email = form.cleaned_data.get("email")
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()
        profile_obj.save()
    context = {"title":"Update Profile", "form":form, "btn_label":"Save"}
    return render(request, "profiles/form.html", context=context)



# Create your views here.
def profile_view(request, username, *args, **kwargs):
    qs = Profile.objects.filter(user__username=username)
    context = {"username":username}
    if not qs.exists():
        raise Http404
    else:
        profile_obj = qs.first()
        user = request.user
        is_following = False
        if user.is_authenticated:
            is_following = user in profile_obj.followers.all()
            # is_following = profile_obj in user.following.all()
            context.update({"is_following":is_following})
        context.update({"profile":profile_obj})
    return render(request, "profiles/profile.html", context=context)


def home_view(request, *args, **kwargs):
    #if not logged in, redirect home view to login
    if not request.user.is_authenticated:
        return login_view(request)

    username = request.user.username
    qs = Profile.objects.filter(user__username=username)
    context = {"username":username}
    if not qs.exists():
        raise Http404
    else:
        profile_obj = qs.first()
        user = request.user
        is_following = False
        is_following = user in profile_obj.followers.all()
        # is_following = profile_obj in user.following.all()
        context.update({"is_following":is_following})
        context.update({"profile":profile_obj})
    return render(request, "pages/feed.html", context=context)