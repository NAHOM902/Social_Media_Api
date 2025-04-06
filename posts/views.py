from django.shortcuts import render, get_object_or_404
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from .models import Post, Follow
from rest_framework import serializers
from .serializers import Postserializer, PostDetailserializer, FollowSerializer
from accounts.views import User
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model



User = get_user_model()


        # CRUD OPERATIONS  👇

class PostCreateView(generics.GenericAPIView):


    queryset = Post.objects.all()
    serializer_class = Postserializer
    permission_classes = [permissions.IsAuthenticated]  

   # GETS ALL POSTS AVAILABLE ...

    def get(self, request):
        posts = Post.objects.all()
        serializer = self.serializer_class(posts, many=True)  # Fixed instance passing

        return Response(serializer.data, status=status.HTTP_200_OK)
    

   # CREATAE A POST...
    
    def post(self, request):
        serializer = self.serializer_class(

            data=request.data,  
            context={'author': request.user} 
        )
        
        user = request.user

        if serializer.is_valid():
            serializer.save(author=user) 

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


                # Post detail, update, and delete view
                        # CRUD OPERATIONS  👇


class PostDetailView(generics.GenericAPIView):

    serializer_class = PostDetailserializer
    permission_classes = (permissions.AllowAny,)

   # GETS DETAIL VIEW WITH AN ID

    def get(self, request, post_id):


        post = get_object_or_404(Post, pk=post_id)
        serializer = self.serializer_class(instance=post)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    # UPDATES A POST WITH A SPECIFIC ID

    def put(self, request, post_id):

        queryset = Post.objects.all()
        serializer_class = PostDetailserializer


        try:
            instance = Post.objects.get(pk=post_id)  # Direct query instead of get_queryset()
        except Post.DoesNotExist:
            return Response(
                {"error": "Post not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
            
        serializer = self.serializer_class(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
   # DELETE A POST WITH AN ID

    def delete(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        
        post.delete()


        return Response(status=status.HTTP_204_NO_CONTENT)
    



class UserPostView(generics.GenericAPIView):
    serializer_class = PostDetailserializer

    def get(self, request, user_id):
        try:
            user = User.objects.get(pk=user_id)
            posts = Post.objects.filter(author=user)  # Assuming Post has an author field
            serializer = self.get_serializer(posts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )


class UserPostDetail(generics.GenericAPIView):
    
    serializer_class = PostDetailserializer

    def get(self, reqeust, user_id, post_id):
        try:
            user = User.objects.get(pk=user_id)
            posts = Post.objects.filter(author=user).filter(pk=post_id)
            serializer = self.get_serializer(posts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )  





    # ------------------_________________________FOLLOWERS SECTION USING GENERICS VIEWS_______________________-----------------------------

# view for following a user

class FollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id, *args, **kwargs):
        try:
            user_to_follow = User.objects.get(pk=user_id)

            if user_to_follow == request.user:
                return Response({'error': "You cannot follow yourself"}, status=status.HTTP_400_BAD_REQUEST)

            # Check if already following
            if Follow.objects.filter(follower=request.user, following=user_to_follow).exists():
                return Response({'message': 'You are already following this user'}, status=status.HTTP_400_BAD_REQUEST)

            Follow.objects.create(follower=request.user, following=user_to_follow)
            return Response({"success": f"You are now following {user_to_follow.username}."}, status=status.HTTP_201_CREATED)

        except User.DoesNotExist:
            return Response({'error': "User not found"}, status=status.HTTP_404_NOT_FOUND)

# view for unfollowing a user

class UnfollowUserView(generics.GenericAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id, *args, **kwargs):
        try:
            user_to_unfollow = User.objects.get(pk=user_id)#Get the user
            if user_to_unfollow == request.user:
                return Response({"error": "You can not unfollow yourself"}, status=status.HTTP_400_BAD_REQUEST)
            
            request.user.following.remove(user_to_unfollow)
            return Response({"success": f"You have unfollow {user_to_unfollow.username}."}, status=status.HTTP_200_OK)
        
        except User.DoesNotExist:
            return Response({"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)
        

# view for listing all users th current user is following
class UserFollowingListView(ListAPIView):
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(followers__follower=self.request.user)
