from django.shortcuts import render
import datetime

post_dummydata = [
    {
        "slug": "apis-in-practice",
        "image": "api-post-image.png",
        "author": "Mohamed Sharif",
        "date": datetime.date(2024, 4, 1),
        "title": "Api in practice",
        "content": "Long content goes here..."

    }
]


def get_date(post):
    return post["date"]


# Create your views here.

def starting_page(request):
    valid_posts = [post for post in post_dummydata if post.get('date') is not None]

    if valid_posts:
        sorted_posts = sorted(valid_posts, key=get_date, reverse=True)
        latest_post = sorted_posts[0]
    else:
        latest_post = None

    return render(request, "blog/index.html", {"latest_post": latest_post})


def posts(request):
    return render(request, "blog/all-posts.html")


def post_detail(request, slug):
    return render(request, "blog/post-detail.html")
