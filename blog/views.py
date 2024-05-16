from django.shortcuts import render, get_object_or_404
from .models import Post


def starting_page(request):
    latest_posts = Post.objects.order_by('-date')[0]
    all_posts = Post.objects.all()
    return render(request, "blog/index.html", {"latest_post": latest_posts, "all_posts": all_posts})


def posts(request):
    all_posts = Post.objects.all()
    return render(request, "blog/all-posts.html", {"all_posts": all_posts})


def post_detail(request, slug):
    identified_post = get_object_or_404(Post, slug=slug)
    return render(request, "blog/post-detail.html", {
        "post": identified_post,
    })
