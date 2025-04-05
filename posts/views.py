from django.shortcuts import render, get_object_or_404
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from .models import Post
from rest_framework import serializers
from .serializers import Postserializer, PostDetailserializer
from accounts.views import User
from rest_framework.decorators import api_view




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