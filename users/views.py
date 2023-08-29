from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, filters
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, ListModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework_simplejwt.views import TokenObtainPairView
from users import serializers
from users import models


class UserLoginView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    

class UserSignupView(APIView):
    serializer_class = serializers.UserSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data
            serializer.save()
            return Response ("Account created successfully") 
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
            
class AddressView(ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = None
    
    def get_queryset(self):
        user = self.request.user
        return models.Address.objects.select_related('user',).filter(user=user)
    
    def get_serializer_context(self):
        context = {'user_id': self.request.user.id,} # type: ignore
        return context
    
    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return serializers.UpdateAddressSerializer
        if self.request.method == 'POST':
            return serializers.AddAddressSerializer
        return serializers.AddressSerializer