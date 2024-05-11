from django.shortcuts import render
from .dummy_data import post_dummydata


def get_date(post):
    return post["date"]


def starting_page(request):
    valid_posts = [post for post in post_dummydata if post.get('date') is not None]

    if valid_posts:
        sorted_posts = sorted(valid_posts, key=get_date, reverse=True)
        latest_post = sorted_posts[0]
    else:
        latest_post = None

    return render(request, "blog/index.html", {"latest_post": latest_post})


def posts(request):
    return render(request, "blog/all-posts.html", {
        "all_posts": post_dummydata,
    })


def post_detail(request, slug):
    identified_post = next(post for post in post_dummydata if post['slug'] == slug)
    return render(request, "blog/post-detail.html", {
        "post": identified_post,
    })
