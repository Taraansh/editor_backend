from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from accounts.models import Profile
from accounts.serializers import ProfileSerializer, MyTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

# Create your views here.
from django.contrib.auth.hashers import make_password, check_password

@api_view(["POST"])
def signup(request):

    email = request.data['email']
    
    if Profile.objects.filter(email=email).exists():
        return JsonResponse({'message': 'Email already exists'})

    if request.method == 'POST':
        user_name = request.data.get('user_name')
        user_contact = request.data.get('user_contact')
        email = request.data.get('email')
        password = request.data.get('password')

        # Create a new Profile instance
        user_password_hashed = make_password(password)
        user = Profile(user_name=user_name, user_contact=user_contact, email=email, password=user_password_hashed)
        user.save()
        serializer = ProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(["POST"])
def loginreq(request):
    if request.method == "POST":
        email = request.data.get('email')
        password = request.data.get('password')
        user = Profile.objects.filter(email=email).first()

        if user is not None and check_password(password, user.password):
            serializer = ProfileSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)
        
@api_view(["PUT", "DELETE"])
def modify(request, email):
    user = get_object_or_404(Profile, email=email)

    if request.method == "PUT":
        user.user_name = request.data.get('user_name', user.user_name)
        user.user_contact = request.data.get('user_contact', user.user_contact)
        user.email = request.data.get('email', user.email)
        user.save()
        serializer = ProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "DELETE":
        user.delete()
        return Response({"detail": "Profile deleted"}, status=status.HTTP_204_NO_CONTENT)
    

@api_view(["GET"])
def profile(request, email):
    user = get_object_or_404(Profile, email=email)
    if user is not None:
        serializer = ProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({"detail": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(["PUT"])
def password_change(request, email):
    user = get_object_or_404(Profile, email=email)
    if request.method == "PUT":
        password = request.data.get('password')
        new_password = request.data.get('new_password')
        # hashed_old_password = make_password(password)
        hashed_new_password = make_password(new_password)
        # if (hashed_old_password == user.password):
        if user.check_password(password):
            user.password = hashed_new_password
            user.save()
            return Response({"detail": "Password Changed Successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Invalid old password"}, status=status.HTTP_401_UNAUTHORIZED)


# view for token routes
@api_view(['GET'])
def get_routes(request):
    """returns a view containing all the possible routes"""
    routes = [
       '/token',
       '/token/refresh'
   ]
    return Response(routes)

# view to customize token
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer