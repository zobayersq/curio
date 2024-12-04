from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import CreateView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from rest_framework import status, views
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
import random
from blog.models import *
from blog.forms import *
from .quotes import quotes

def blog_index(request):
    posts = Post.objects.all().order_by("-created_on")
    quote = random.choice(quotes)
    context = {
        "posts":posts,
        "quote": quote,
    }
    return render(request, "blog/index.html", context)

def blog_category(request, category):
    posts = Post.objects.filter(
        categories__name__contains=category
    ).order_by("-created_on")
    context = {
        "category":category,
        "posts":posts,
    }
    return render(request, "blog/category.html", context)



def blog_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = CommentForms()
    if request.method == "POST":
        form = CommentForms(request.POST)
        if form.is_valid():
            comment = Comment(
                author = form.cleaned_data["author"],
                body=form.cleaned_data["body"],
                post=post,
            )
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
        return HttpResponseRedirect(request.path_info)
    else:
        form = CommentForms()

    comments = Comment.objects.filter(post=post)
    context = {
        "post":post,
        "comments":comments,
        "form":CommentForms(),
    }
    return render(request, "blog/detail.html", context)

def blog_category_list(request):
    categories = Category.objects.all().order_by("name")
    posts=Post.objects.all().order_by('-created_on')
    context = {
        "categories":categories,
        "posts":posts,

    }
    return render(request, "blog/category_list.html", context)


@method_decorator(login_required, name='dispatch')
class CreateBlogView(CreateView):
    model = Post
    form_class = PostForms
    template_name = 'blog/write_story.html'
    success_url = '../'  # Replace with your desired redirect URL

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


@login_required
def profile(request):
    # Get the current logged-in user
    user = request.user
    try:
        # Retrieve the UserProfile or create one if it doesn't exist
        profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        profile = None

    context = {
        'user': user,
        'profile': profile,
    }
    return render(request, 'blog/profile.html', context)



def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "You have successfully logged in!")
            return redirect('blog_index')  # Redirect to your desired page after login
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'blog/login.html', {'form': form})

# View for user signup

def user_signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Your account has been created successfully!")
                return redirect('blog_index')
            else:
                messages.error(request, "There was an error logging in after signup.")
        else:
            messages.error(request, "Error creating account. Please try again.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'blog/signup.html', {'form': form})

# View for user logout
def user_logout(request):
    logout(request)
    messages.success(request, "You have logged out successfully.")
    return redirect('blog_index')  # Redirect to your desired page after logout


@login_required
@csrf_exempt
def love_post(request, pk):
    if request.method == 'POST':
        post = Post.objects.get(pk=pk)
        user = request.user

        if user in post.love_reactions.all():
            post.love_reactions.remove(user)
            loved = False
        else:
            post.love_reactions.add(user)
            loved = True

        new_love_count = post.get_love_count()
        return JsonResponse({
            'success': True,
            'loved': loved,
            'new_love_count': new_love_count
        })

# API view for user signup
class UserSignupView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        form = UserCreationForm(data=request.data)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return Response({"message": "User created and logged in successfully!"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"error": "Authentication failed after signup."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Invalid data provided."}, status=status.HTTP_400_BAD_REQUEST)

# API view for user login
class UserLoginView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        form = AuthenticationForm(data=request.data)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return Response({"message": "Logged in successfully!"}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid username or password."}, status=status.HTTP_400_BAD_REQUEST)

# API view for user logout
class UserLogoutView(views.APIView):
    def post(self, request):
        logout(request)
        return Response({"message": "Logged out successfully!"}, status=status.HTTP_200_OK)
