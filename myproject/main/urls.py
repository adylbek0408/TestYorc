from django.urls import path
from . import views


urlpatterns = [
    # Category Endpoints
    path('categories/', views.CategoryListCreateView.as_view(), name='category-list-create'),

    path('products/', views.ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),

    path('comments/', views.CommentListCreateView.as_view(), name='comment-list-create'),

    path('products/<int:product_id>/like/', views.LikeProductView.as_view(), name='like-product'),
    path('products/<int:product_id>/favorite/', views.FavoriteProductView.as_view(), name='favorite-product'),

]
