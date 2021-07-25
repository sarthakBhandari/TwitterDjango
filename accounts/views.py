from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout, authenticate


# Create your views here.
def login_view(request, *args, **kwargs):
    form = AuthenticationForm(request, data=request.POST or None)
    if form.is_valid():
        user_ = form.get_user()
        login(request, user_)
        return redirect("/")
    context = {"form":form, "btn_label":"Login", "title":"Login"}
    return render(request, "accounts/auth.html", context=context)

def logout_view(request, *args, **kwargs):
    if request.method == "POST":
        logout(request)
        return redirect("/login")
    context = {"form":None, "btn_label":"Click to Cofirm", "title":"Logout", "description":"Are you sure you want to logout"}
    return render(request, "accounts/auth.html", context=context)

def register_view(request, *args, **kwargs):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=True)
        user.set_password(form.cleaned_data.get('password1'))
        #username = forms.cleaned_data.get("username")
        #User.objects.create(username=username)
        login(request, user)
        return redirect("/")

    context = {"form":form, "btn_label":"Register", "title":"Register"}
    return render(request, "accounts/auth.html", context=context)