from .models import User
from .serializers import SignUpSerializer, UserSerializer
from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import ModelViewSet


class SignUpView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    """def create(self, request, *args, **kwargs):
        print("Received data:", request.data)
        print("Using serializer:", self.get_serializer_class())

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(status=status.HTTP_201_CREATED) """


class UserView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    search_fields = ["first_name", "last_name", "email"]
    filterset_fields = ["email", "first_name", "last_name", "role"]
