from django.urls import path
from webpages import views

urlpatterns = [
    path('savepage/<str:email>/', views.save_page, name='save_page'),
    path('viewallpages/<str:email>/', views.view_all_pages, name='view_all_pages'),
    path('delete/<int:id>/', views.delete_page, name='delete_page'),
    path('modify/<int:id>/', views.modify_page, name='modify_page'),
]
