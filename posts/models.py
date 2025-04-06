from django.db import models
from accounts.models import User



class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"posted by {self.author.username} - {self.timestamp}"
    

class Follow(models.Model):
    follower = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name='following' )
    following = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name='followers' )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"