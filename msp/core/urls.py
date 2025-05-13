from django.urls import path
from . import views, api_views

urlpatterns = [
    path('track/<str:code>/', views.track_product_view, name='track-product'),
    path('api/code/<str:code>/', api_views.MarkingCodeDetailView.as_view(), name='api-code-detail'),
    path('api/code/<str:code>/move/', api_views.AddMovementView.as_view(), name='api-code-move'),
    path('api/locations/', api_views.LocationListView.as_view(), name='api-locations'),
    path('api/batches/', api_views.ProductBatchListView.as_view(), name='api-batches'),
    path('api/batches/<int:batch_id>/codes/', api_views.BatchCodesView.as_view(), name='api-batch-codes'),
]