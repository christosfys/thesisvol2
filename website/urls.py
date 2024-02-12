from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('segmentation/', views.category, name='category'),
    path('segmentation/<str:model_name>/', views.model_details, name='model_details'),
    # path('download/', views.download_model, name='download_model'),
    path('download/<str:model_name>/', views.download_model, name='download_model'),    
    path('roles/', views.role_display, name='roles'),
 ]
