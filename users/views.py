from rest_framework.response import Response
from rest_framework import status
from .serializers import SignUpSerializer
from rest_framework.generics import CreateAPIView


class SignUpView(CreateAPIView):
    serializer_class = SignUpSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)
