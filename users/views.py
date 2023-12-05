from rest_framework import mixins, status, viewsets
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from users import models
from users.serializers import AddressSerializer, UserSerializer

# class UserLoginView(ObtainAuthToken):
#     renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class UserSignupView(viewsets.GenericViewSet, mixins.CreateModelMixin):
    serializer_class = UserSerializer
    queryset = models.User.objects.all()
    permission_classes = ()


class AddressView(ModelViewSet):
    serializer_class = AddressSerializer
    pagination_class = None

    def get_queryset(self):
        user = self.request.user
        return models.Address.objects.select_related(
            "user",
        ).filter(user=user)
