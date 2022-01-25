import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.views.generic import ListView
from .models import User, Post

# FOR: Paginator and Listview: https://docs.djangoproject.com/en/3.0/topics/pagination/
class PostList(ListView):
    paginate_by = 2
    model = Post

def index(request):
    posts = Post.objects.all();
    if request.method == "POST":
        likes=request.POST.get("likes", "")
        content=request.POST.get("post", "")
        user=User.objects.get(id=request.user.id)
        post = Post(
                user=request.user,
                likes=likes,
                content=content,
                
               )
        post.save()
        
    posts=Post.objects.all()  
    posts = posts.order_by("-timestamp").all()
    paginator = Paginator(posts, 2) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number) 
    return render(request, "network/index.html", {
        "posts": posts,
        "page_obj": page_obj
        })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("network:index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("network:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("network:index"))
    else:
        return render(request, "network/register.html")


def profile(request):

    user=User.objects.get(id=request.user.id)
    posts=Post.objects.filter( user=request.user )
    posts=posts.order_by("-timestamp").all() 
    
    followers_count=Post.objects.filter(user=request.user).exclude(follower=request.user).count()
    following = Post.objects.exclude(user=request.user).filter(follower=request.user).count()

    # for foll in following:
    #     for fol in foll:
    #         print(fol[0])
    return render(request, "network/profile.html",{
        "posts":posts,
        "followers": followers_count,
        "following": following
        })

@csrf_exempt
@login_required
def like(request,pk):
    if request.method == "PUT":
        post=Post.objects.get(id=pk)
        likes=post.likes + 1
        Post.objects.filter(id=pk).update(likes=likes)
        return JsonResponse({"likes": likes})
 
@csrf_exempt
@login_required   
def unlike(request,pk):
    if request.method == "PUT":
        post=Post.objects.get(id=pk)
        likes=post.likes - 1
        print(f"likes: {likes}")
        Post.objects.filter(id=pk).update(likes=likes)
        return JsonResponse({"likes": likes})

@csrf_exempt
@login_required  
def following(request,pk):
    if request.method == "PUT":
       data = json.loads(request.body)
       post_id= data["post_id"]
       user= User.objects.get(id=request.user.id)
       post=Post.objects.get(id=post_id)

       posts=user.followers.all()

       if post not in posts:
        user.followers.add(post)
       following=Post.objects.filter(follower=request.user.id).all()
       print(f"following are {following}")
       user.save()
       foll = user.followers.all()
       print(f"followers are {foll}")
       for fol in foll:
        print(f"follower is  {fol.user_id}")
       return JsonResponse({"follower": user.id})

    posts=Post.objects.filter(follower=request.user)

    following=[]
    for post in posts:
        if post.user not in following:
            following.append(post.user)

    num_following = len(following)

    return render(request, "network/following.html",{
            "posts": posts,
            "following":num_following
        })

@csrf_exempt
@login_required 
def unfollowing(request,pk):
    if request.method == "PUT":
       data = json.loads(request.body)
       post_id= data["post_id"] 
       post=Post.objects.get(id=post_id) 
       user= User.objects.get(id=request.user.id)
       users = user.followers.all()
       for use in users:
        print(f"Before is {use.user_id}")
       user.followers.remove(post)
       users = user.followers.all()
       for use in users:
        print(f"After is {use.user_id}")
       return JsonResponse({"follower": user.id})

@csrf_exempt
@login_required 
def edit(request, pk):

    data = json.loads(request.body)
    text=data["text"]
    if request.method == "PUT":
       Post.objects.filter(id=pk).update(content=text)
       print(data["text"])
       return JsonResponse({"text": text})
    else:
        return JsonResponse({"text": text})



