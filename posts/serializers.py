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