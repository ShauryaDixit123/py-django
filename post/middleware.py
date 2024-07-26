from django.http import HttpResponse, HttpRequest,JsonResponse
from .models import User, Post, Comment


class AuthMiddleWare:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if(request.path == '/api/users/'): return response
        auth = request.headers.get("authorization")
        if auth is None:
            return HttpResponse("Token is required!")
        usr = User.objects.filter(tkn__exact=auth).first()
        if usr is None:
            return HttpResponse("Invalid Token!")
        return response