from django.shortcuts import render
from .models import User
from .serializers import RegistrationSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework import serializers
from drf_yasg.utils import swagger_auto_schema



class RegisterViews(generics.GenericAPIView):

    serializer_class = RegistrationSerializer

    @swagger_auto_schema(operation_summary="create a user account")

    def post(self, request):
        data = request.data
        

        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "Message": "😁 user created successfully 😁",
                "user": serializer.data}, status=status.HTTP_201_CREATED
                )
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 