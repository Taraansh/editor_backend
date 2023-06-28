from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from accounts.models import Profile
from accounts.serializers import ProfileSerializer

# Create your views here.
from django.contrib.auth.hashers import make_password, check_password

@api_view(["POST"])
def signup(request):
    if request.method == 'POST':
        user_name = request.data.get('user_name')
        user_contact = request.data.get('user_contact')
        user_email = request.data.get('user_email')
        user_password = request.data.get('user_password')

        # Create a new Profile instance
        user_password_hashed = make_password(user_password)
        user = Profile(user_name=user_name, user_contact=user_contact, user_email=user_email, password=user_password_hashed)
        user.save()
        serializer = ProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(["POST"])
def loginreq(request):
    if request.method == "POST":
        user_email = request.data.get('user_email')
        password = request.data.get('password')
        user = Profile.objects.filter(user_email=user_email).first()

        if user is not None and check_password(password, user.password):
            serializer = ProfileSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)
        
@api_view(["PUT", "DELETE"])
def modify(request, email, password):
    user = get_object_or_404(Profile, user_email=email, user_password=password)

    if request.method == "PUT":
        user.user_name = request.data.get('user_name', user.user_name)
        user.user_contact = request.data.get('user_contact', user.user_contact)
        user.user_email = request.data.get('user_email', user.user_email)
        new_password = request.data.get('new_password')
        if new_password:
            user.set_password(new_password)  # Hash the new password using set_password method
        user.save()
        serializer = ProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "DELETE":
        user.delete()
        return Response({"detail": "Profile deleted"}, status=status.HTTP_204_NO_CONTENT)
    

@api_view(["GET"])
def profile(request, email, password):
    user = get_object_or_404(Profile, user_email=email)
    
    # Check if the provided password matches the user's hashed password
    if user.check_password(password):
        serializer = ProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({"detail": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)
