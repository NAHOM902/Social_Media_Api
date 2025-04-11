from django.shortcuts import render, get_object_or_404
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from .models import Post, Follow, Comment, like
from rest_framework import serializers
from .serializers import Postserializer, PostDetailserializer, FollowSerializer, CommentSerializer, LikeSerializer
from accounts.views import User
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema 
from rest_framework.exceptions import ValidationError



User = get_user_model()


        # CRUD OPERATIONS  👇

class PostCreateView(generics.GenericAPIView):


    queryset = Post.objects.all()
    serializer_class = Postserializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  

   # GETS ALL POSTS AVAILABLE ...

    @swagger_auto_schema(operation_summary="List all Posts made ")

    def get(self, request):
        posts = Post.objects.all()
        serializer = self.serializer_class(posts, many=True)  # Fixed instance passing

        return Response(serializer.data, status=status.HTTP_200_OK)
    

   # CREATAE A POST...

    @swagger_auto_schema(operation_summary="Create a new post ")

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
    permission_classes = [IsAuthenticated]

   # GETS DETAIL VIEW WITH AN ID

    @swagger_auto_schema(operation_summary="Retrive a post by it's id")

    def get(self, request, post_id):


        post = get_object_or_404(Post, pk=post_id)
        serializer = self.serializer_class(instance=post)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    # UPDATES A POST WITH A SPECIFIC ID

    @swagger_auto_schema(operation_summary="update a post by it's id")


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

    @swagger_auto_schema(operation_summary="Delete a post by it's id")

    def delete(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        
        post.delete()


        return Response(status=status.HTTP_204_NO_CONTENT)
    



class UserPostView(generics.GenericAPIView):
    serializer_class = PostDetailserializer
    
    @swagger_auto_schema(operation_summary="Get all posts for a user")

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

    @swagger_auto_schema(operation_summary="GET a user's specific post")

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
      
    @swagger_auto_schema(tags=["Follow"])

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

    @swagger_auto_schema(tags=["Follow"])
    def post(self, request, user_id, *args, **kwargs):
        try:
            user_to_unfollow = User.objects.get(pk=user_id)#Get the user
            if user_to_unfollow == request.user:
                return Response({"error": "You can not unfollow yourself"}, status=status.HTTP_400_BAD_REQUEST)
            follow_instance = Follow.objects.filter(follower=request.user, following=user_to_unfollow).first()
            if not follow_instance:
                return Response({"error": "You are not following this user"}, status=status.HTTP_400_BAD_REQUEST)

            follow_instance.delete()
            return Response({"success": f"You have unfollowed {user_to_unfollow.username}."}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)
        

# view for listing all users th current user is following
class UserFollowingListView(ListAPIView):
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(tags=["Follow"])


    def get_queryset(self):
        return User.objects.filter(followers__follower=self.request.user)
    



        # comments section

class CommentListCreateApiView(generics.ListCreateAPIView):

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_class = [permissions.IsAuthenticatedOrReadOnly]


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):

        if self.request.user != self.get_object().user:
            raise PermissionError("You can't edit someone else's comment.")
        serializer.save()
    
    def perform_destroy(self, instance):
        if self.request.user != self.get_object().user:
            raise PermissionError("you can't delete someone else's comment.")
        instance.delte()


             #like a post

class LikeCreateApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
            user = request.user

                    # Check if the user has already liked the post
            if like.objects.filter(post=post, user=user).exists():
                return Response({'error': "You have already liked this post"}, status=status.HTTP_400_BAD_REQUEST)
            
             # Create a like
            new_like, created = like.objects.get_or_create(user=user, post=post)

            # Serialize the newly created like
            serializer = LikeSerializer(new_like)

            # Extract data to show nice message
            data = serializer.data
            msg = f"{data['author_username']} liked  this spost 🤙 '{data['post_id']}' created by {data['post_author']}"
            return Response({"message": msg}, status=status.HTTP_201_CREATED)
        
        except Post.DoesNotExist:
            return Response({'error post not found'}, status=status.HTTP_404_NOT_FOUND)


   
class unlike(generics.GenericAPIView):
    queryset = Post.objects.all()  # Query for the Post model
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            # post = self.get_object()  # Get the Post object using `pk`
            post = generics.get_object_or_404(Post, pk=pk)
            user = request.user

            # Check if the user has liked the post
            likes = like.objects.filter(post=post, user=user).first()
            if not likes:
                return Response({"error": "You haven't liked this post"}, status=status.HTTP_400_BAD_REQUEST)

            # Remove the like
            likes.delete()

            return Response({"success": "Post unliked successfully"}, status=status.HTTP_200_OK)

        except Post.DoesNotExist:
            return Response({'error': "Post does not exist"}, status=status.HTTP_404_NOT_FOUND)

