from django.http import JsonResponse

def home(request):
    views = [
        'profile/<str:email>/', # Send a GET request with email to get user profile
        'modify/<str:email>/', # Send a PUT/DELETE request with email to change username and password/delete profile
        'loginreq/', # Send a POST request to login
        'signup/', # Send a POST request to register
        'tokensroutes/', # Send a GET request to get all token routes
        'token/',
        'token/refresh/', # Url to get access token using refresh token
        'passchange/<str:email>/', # Send a PUT request with email to change the password

        'savepage/<str:email>/', # Send a POST request with email to save a page
        'viewallpages/<str:email>/', # Send a GET request with email to get all pages created with respective email
        'delete/<int:id>/', # Send a DELETE request with page id to delete the page
        'modify/<int:id>/', # Send a PUT request with page id to modify the page

    ]