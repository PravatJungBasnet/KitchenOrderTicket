from rest_framework.response import Response
from .models import User
from rest_framework.decorators import action
from .serializers import SignUpSerializer, UserSerializer
from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


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
    permission_class = IsAuthenticated

    @action(
        detail=False,
        methods=["get", "put", "patch"],
        name="View/Update Profile",
    )
    def profile(self, request, pk=None):
        user = request.user
        if request.method == "GET":
            serializer = self.get_serializer(user)
            return Response(serializer.data)

        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=status.HTTP_200_OK)

        return Response(
            {
                "errors": "[Validation failed.]",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
