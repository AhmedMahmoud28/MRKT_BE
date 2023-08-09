from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, filters
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from users import serializers
from users import models
from users import permissions


class UserLogin(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    

class UserSignup(APIView):
    serializer_class = serializers.userserializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data
            serializer.save()
            return Response ("Account created successfully") 
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        
