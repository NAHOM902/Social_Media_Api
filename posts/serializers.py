from .models import Post, User, Comment, like
from rest_framework import serializers


# Post Serializer

class Postserializer(serializers.ModelSerializer):
    post_id = serializers.ReadOnlyField(source='id')  #rename id to post_id for better clarity post id

    class Meta:
        model = Post
        fields = ['post_id', 'author', 'content', 'bio', 'profile_picture', 'timestamp']
        read_only_fields = ['author', 'timestamp']  #this fields can't be set by api users
        depth = 1  #shows authors username..




class PostDetailserializer(serializers.ModelSerializer):
    post_id = serializers.ReadOnlyField(source='id')  #rename id to post_id for better clarity post id

    class Meta:
        model = Post
        fields = ['post_id', 'author', 'content', 'timestamp']
        depth = 1  #shows authors username..

        

        #  SERALIZER CLASS FOR FOLLOWERS

class FollowSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'followers', 'following']
        read_only_fields = ['id', 'username', 'followers']

    def update(self, instance, validated_data):
        # Only allow updates to the `following` field
        following = validated_data.pop('following', [])
        instance.following.set(following)
        return instance
    

class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='user.username', read_only=True)
    post_title = serializers.CharField(source='post.content', read_only=True)
    class Meta:
        model = Comment
        fields = ['id', 'user', 'author_username', 'post', 'post_title', 'comment', 'created_at']
        read_only_fields = ['id', 'user', 'create_at']
    

class LikeSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source="user.username", read_only=True)
    post_author = serializers.CharField(source="post.author.username", read_only=True)  
    class Meta:
        model = like
        fields = ['id', 'author_username', 'post_id', 'created_at', 'post_author']
        read_only_fields = ['id', 'author_username', 'created_at']