from django.shortcuts import render
from blog.models import Post, Comment, Category
from django.http import HttpResponseRedirect
from blog.forms import CommentForms

def blog_index(request):
    posts = Post.objects.all().order_by("-created_on")
    context = {
        "posts":posts,
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
    post = Post.objects.get(pk=pk)
    form = CommentForms()
    if request.method == "POST":
        form = CommentForms(request.POST)
        if form.is_valid():
            comment = Comment(
                author = form.cleaned_data["author"],
                body=form.cleaned_data["body"],
                post=post,
            )
        comment.save()
        return HttpResponseRedirect(request.path_info)

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
