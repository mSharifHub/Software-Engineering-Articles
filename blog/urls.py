from django.urls import path
from . import views

urlpatterns = [
    path("", views.starting_page, name="starting-page"),  # root
    path("posts", views.posts, name="post-page"),  # /root/posts
    path("posts/<slug:slug>", views.post_detail, name="post-detail-page")  # /root/post/my-first-post
]
