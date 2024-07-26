from django.db import models
import uuid
# Create your models here.

class User(models.Model):
    id = models.UUIDField(auto_created=True,unique=True,default=uuid.uuid4,primary_key=True)
    name = models.CharField(max_length=50)
    tkn = models.UUIDField(auto_created=True,unique=True,default=uuid.uuid4)
    created_on = models.DateTimeField(auto_now_add=True)
    def __str__(self) -> str:
        return self.id

class Post(models.Model):
    id = models.UUIDField(auto_created=True,unique=True,default=uuid.uuid4,primary_key=True)
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=200)
    likes = models.IntegerField(default=0)
    author_id = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    def __str__(self) -> str:
        return self.id

class Comment(models.Model):
    id = models.UUIDField(auto_created=True,unique=True,default=uuid.uuid4,primary_key=True)
    text = models.CharField(max_length=100)
    author_id = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post,on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)


