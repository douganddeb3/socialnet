from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts")
    likes = models.IntegerField(default=0, blank=True)
    content = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    follower = models.ForeignKey("User", on_delete=models.CASCADE, blank=True, null=True, related_name="followers")

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user,
            "likes": self.likes,
            "content": self.content,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "follower": self.id
   
        }