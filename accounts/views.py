from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User

from .serializers import RegisterSerializer, UserSerializer
# Create your views here.

# REGISTER
@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()
        return Response({
            "message": "User created",
            "user": UserSerializer(user).data
        })

    return Response(serializer.errors, status=400)


# PROFILE (GET + UPDATE)
@api_view(["GET", "PUT"])
@permission_classes([IsAuthenticated])
def profile(request):
    if request.method == "GET":
        return Response(UserSerializer(request.user).data)

    elif request.method == "PUT":
        user = request.user
        user.username = request.data.get("username", user.username)
        user.save()

        return Response({
            "message": "Profile updated",
            "user": UserSerializer(user).data
        })


# LOGOUT (client-side for JWT)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    return Response({
        "message": "Logout successful (delete token on client)"
    })
