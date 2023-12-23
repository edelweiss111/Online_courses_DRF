from django.shortcuts import render
from rest_framework import viewsets, generics

from users.permissions import IsOwner
from users.models import User
from users.serializers import UserSerializer, OwnerSerializer


class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = OwnerSerializer
    queryset = User.objects.all()
    permission_classes = [IsOwner]


class UserRetrieveAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.request.user == self.get_object():
            return OwnerSerializer
        return UserSerializer

