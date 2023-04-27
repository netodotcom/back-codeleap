from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import Post

class UserSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.ReadOnlyField()
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        password = validated_data.pop('password')
        hashed_password = make_password(password)
        validated_data['password'] = hashed_password
        return super().create(validated_data)

    class Meta:
        model = User
        fields = ['id', 'url', 'username', 'email', 'password']

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'username', 'created_datetime', 'title', 'content')

