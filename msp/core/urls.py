from django.urls import path
from . import views

urlpatterns = [
    path('track/<str:code>/', views.track_product_view, name='track-product'),
]