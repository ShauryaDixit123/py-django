from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, JsonResponse
from .models import User, Post, Comment
from django.views.decorators.csrf import csrf_exempt
import json
import uuid

@csrf_exempt
def members(request):
    return HttpResponse("Hello world!")

def get_author_from_token(request):
    tkn = request.headers.get("Authorization")
    return User.objects.filter(tkn__exact=tkn).first()

def createPost(request):
    usr = get_author_from_token(request)
    pst = json.loads(request.body)
    post = Post.objects.create(title=pst["title"], content=pst["content"], author_id=usr)
    post_dict = {
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "likes": post.likes,
        "created_on": post.created_on
    }
    return JsonResponse(post_dict, safe=False)

def getPosts(request):
    posts = Post.objects.all()
    pg = request.GET.get('pg')
    if pg is not None:
        pg = int(pg)
        posts = posts[pg*10:pg*10+10]
    posts_list = list(posts.values())
    return JsonResponse(posts_list, safe=False)

def getPost(request):
    if(request.GET.get('id') is None): return HttpResponse("Id is required")
    id_str = request.GET.get('id')
    res = Post.objects.get(pk=id_str)
    cmts = Comment.objects.filter(post_id__exact=uuid.UUID(id_str))
    cmts_list = list(cmts.values())
    res_dict = {"id": res.id, "title": res.title, "content": res.content,"likes":res.likes, "created_on": res.created_on,"comments" : cmts_list}
    return JsonResponse(res_dict, safe=False)

def updatePost(request):
    usr = get_author_from_token(request)
    pst = json.loads(request.body)
    post = Post.objects.get(pk=pst["id"])
    post.title = pst["title"]
    post.content = pst["content"]
    post.author = usr
    post.save()
    return JsonResponse({"data": "Post updated successfully"})

def deletePost(request):
    id_str = json.loads(request.body)["id"]
    Post.objects.get(pk=id_str).delete()
    return JsonResponse({"data": "Post deleted successfully"})

def createUser(request):
    py = json.loads(request.body)
    res = User.objects.create(name=py["name"])
    res_dict = {"id": res.id, "name": res.name, "tkn": res.tkn}
    return JsonResponse(res_dict, safe=False)

def getUser(request):
    if(request.GET.get('id') is None): return HttpResponse("Id is required")
    id_str = request.GET.get('id')
    res = User.objects.get(pk=id_str)
    res_dict = {"id": res.id, "name": res.name, "tkn": res.tkn, "created_on": res.created_on}
    return JsonResponse(res_dict, safe=False)

def getUsers(request):
    users = User.objects.all()
    users_list = list(users.values())
    return JsonResponse(users_list, safe=False)

def createComment(request):
    usr = get_author_from_token(request)
    cmt = json.loads(request.body)
    pst = Post.objects.get(pk=cmt["post_id"])
    res = Comment.objects.create(post_id=pst, author_id=usr, text=cmt["text"])
    res_dict = {"id": res.id, "text": res.text, "created_on": res.created_on}
    return JsonResponse(res_dict, safe=False)

def updateComment(request):
    usr = get_author_from_token(request)
    cmt = json.loads(request.body)
    comment = Comment.objects.get(pk=cmt["id"])
    comment.content = cmt["content"]
    comment.user = usr
    comment.save()
    return JsonResponse({"data": "Comment updated successfully"})

def deleteComment(request):
    id_str = json.loads(request.body)["id"]
    Comment.objects.get(pk=id_str).delete()
    return JsonResponse({"data": "Comment deleted successfully"})

def addLikeToPost(request):
    id_str = request.GET.get('id')
    pst = Post.objects.get(pk=id_str)
    pst.likes = pst.likes + 1
    pst.save()
    return JsonResponse({"data": "Liked successfully"})


def User_CRUD_handler(request):
    if request.method == "POST":
        return createUser(request)
    if request.method == "GET":
        return getUser(request)

def Post_CRUD_handler(request):
    if request.method == "POST":
        return createPost(request)
    if request.method == "GET":
        return getPost(request)
    if request.method == "PUT":
        return updatePost(request)
    if request.method == "DELETE":
        return deletePost(request)

def Comment_CRUD_handler(request):
    if request.method == "POST":
        return createComment(request)
    if request.method == "PUT":
        return updateComment(request)
    if request.method == "DELETE":
        return deleteComment(request)