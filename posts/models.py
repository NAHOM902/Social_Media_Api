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
    

class Comment(models.Model):

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE , related_name="comments")
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"comment by {self.author} on {self.post}"



class like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')  # A user can only like a post once.

    def __str__(self):
        return f"{self.user.username} likes {self.post.title}"