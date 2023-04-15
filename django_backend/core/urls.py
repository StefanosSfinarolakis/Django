from django.urls import path
from . import views

urlpatterns = [
    path('image-upload/', views.image_upload_view, name='image_upload'),
    path('image-list/', views.image_list_view, name='image_list'),
    path('image-detail/<int:pk>/', views.image_detail_view, name='image_detail'),
]