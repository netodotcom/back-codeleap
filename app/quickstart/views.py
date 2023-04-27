import json
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password, check_password

from .models import Post
from .serializers import UserSerializer
from .serializers import PostSerializer

class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        password = serializer.validated_data.pop('password')
        serializer.save(password=password)

class UserLogin(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user and check_password(password, user.password):
            token = Token.objects.filter(user=user).first()
            if not token:
                token = Token.objects.create(user=user)
            return Response({'id': user.id, 'username': user.username, 'token': token.key})
        else:
            return Response({'error': 'Invalid username or password'},
                            status=status.HTTP_400_BAD_REQUEST)

class UserLogout(generics.GenericAPIView):
    def post(self, request):
        try:
            token = request.META['HTTP_AUTHORIZATION'].split(' ')[1]
            auth_token = Token.objects.get(key=token)
            auth_token.delete()
            return Response({"message": "User logged out successfully."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class IsTokenValid(generics.GenericAPIView):
    def post(self, request):
        data = request.body.decode('utf-8')
        json_data = json.loads(data)
        token = json_data.get('token')
        if token is None:
            return Response({"error": "Invalid token."}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            Token.objects.get(key=token)
            return Response({"token": "Valid token"}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({"error": "Invalid token."}, status=status.HTTP_401_UNAUTHORIZED)

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer