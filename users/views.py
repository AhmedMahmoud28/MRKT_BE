from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from users import models, serializers

# class UserLoginView(ObtainAuthToken):
#     renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class UserSignupView(APIView):
    serializer_class = serializers.UserSerializer
    permission_classes = ()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.validated_data
            serializer.save()
            return Response("Account created successfully")
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddressView(ModelViewSet):
    serializer_class = serializers.AddressSerializer
    pagination_class = None

    def get_queryset(self):
        user = self.request.user
        return models.Address.objects.select_related(
            "user",
        ).filter(user=user)
