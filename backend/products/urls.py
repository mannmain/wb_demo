from django.urls import path

from products.views import ColorVariantViewSet, BrandViewSet, ColorViewSet, KindViewSet, ColorVariantDetailsViewSet

urlpatterns = [
    path('products/', ColorVariantViewSet.as_view({'get': 'list'})),
    path('products/<int:pk>/', ColorVariantDetailsViewSet.as_view({'get': 'retrieve'}), name='colorvariant-detail'),
    path('brands/', BrandViewSet.as_view({'get': 'list'})),
    path('colors/', ColorViewSet.as_view({'get': 'list'})),
    path('kinds/', KindViewSet.as_view({'get': 'list'})),
]
