from django.urls import path
from accounts import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('profile/<str:email>/', views.profile, name="profile"),
    path('modify/<str:email>/', views.modify, name="modify"),
    path('loginreq/', views.loginreq, name="loginreq"),
    path('signup/', views.signup, name='signup'),
    # token paths
    path('tokensroutes/', views.get_routes, name='token_routes'),
    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]