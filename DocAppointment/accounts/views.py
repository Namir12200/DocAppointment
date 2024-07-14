from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserSerializer, ProfileSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Profile
from .tasks import send_user_registration_mail
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .permissions import IsUserOwnerOrReadOnly, IsProfileOwnerOrReadOnly
from django.contrib.auth.hashers import make_password
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
# Create your views here.

class UserListView(APIView):
    def post(self, request):
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid():
            user_serializer.validated_data['password'] = make_password(user_serializer.validated_data['password'])
            user = user_serializer.save()
            
            send_user_registration_mail.delay_on_commit(user.email)
            refresh = RefreshToken.for_user(user)

            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }, status=status.HTTP_201_CREATED)
        
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @method_decorator(cache_page(60 * 60 * 2))    
    def get(self, request):
        users = User.objects.all()
        user_serializer = UserSerializer(users, many=True)
        return Response(user_serializer.data)
    
class UserDetailView(APIView):
    permission_classes = [IsAuthenticated, IsUserOwnerOrReadOnly]

    def get_object(self, pk):
        obj = get_object_or_404(User, pk=pk)
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request, pk):
        user = self.get_object(pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk):
        user = self.get_object(pk=pk)
        print(request.user == user)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            if 'password' in serializer.validated_data:
                serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = self.get_object(pk=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class ProfileListView(APIView):
    @method_decorator(cache_page(60 * 60 * 2))
    def get(self, request):
        profile = Profile.objects.all()
        profile_serializer = ProfileSerializer(profile, many=True)
        return Response(profile_serializer.data)
    
    def post(self, request):
        profile_serializer = ProfileSerializer(data=request.data)
        if profile_serializer.is_valid():
            profile_serializer.save()
            return Response(profile_serializer.data)
        return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ProfileDetailView(APIView):
    permission_classes = [IsAuthenticated, IsProfileOwnerOrReadOnly]

    def get_object(self, pk):
        profile = get_object_or_404(Profile, pk=pk)
        self.check_object_permissions(self.request, profile)
        return profile
    
    def get(self, request, pk):
        profile = self.get_object(pk=pk)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)
    
    def put(self, request, pk):
        profile = self.get_object(pk=pk)
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        profile = self.get_object(pk=pk)
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)