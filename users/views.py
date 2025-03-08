from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import SignUpSerializer, UserSerializer
from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import ModelViewSet


class SignUpView(CreateAPIView):
    serializer_class = SignUpSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)


class UserView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    search_fields = ["first_name", "last_name", "email"]
    filterset_fields = ["email", "first_name", "last_name", "role"]
