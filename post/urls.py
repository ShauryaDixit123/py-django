from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("posts/", views.Post_CRUD_handler),
    path("users/", views.User_CRUD_handler),
    path("posts/comments/", views.Comment_CRUD_handler),
    path("users/all/", views.getUsers),
    path("posts/all/", views.getPosts),
    path("posts/like/", views.addLikeToPost),

]
