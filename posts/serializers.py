from .models import Post, User
from rest_framework import serializers


# Post Serializer

class Postserializer(serializers.ModelSerializer):
    post_id = serializers.ReadOnlyField(source='id')  #rename id to post_id for better clarity post id

    class Meta:
        model = Post
        fields = ['post_id', 'author', 'content', 'timestamp']
        read_only_fields = ['author', 'timestamp']  #this fields can't be set by api users
        depth = 1  #shows authors username..




class PostDetailserializer(serializers.ModelSerializer):
    post_id = serializers.ReadOnlyField(source='id')  #rename id to post_id for better clarity post id

    class Meta:
        model = Post
        fields = ['post_id', 'author', 'content', 'timestamp']
        depth = 1  #shows authors username..

        