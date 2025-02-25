from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from .models import Category, Product, Favorite, Like, Comment
from .serializers import CategorySerializer, ProductSerializer, CommentSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]


class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at']
    permission_classes = [IsAuthenticated]


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        product_id = self.request.query_params.get('product_id')
        if product_id:
            return Comment.objects.filter(product_id=product_id)
        return Comment.objects.all()

    def perform_create(self, serializer):
        # Автоматически устанавливаем текущего пользователя
        serializer.save(user=self.request.user)


class LikeProductView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        like, created = Like.objects.get_or_create(user=request.user, product=product)
        if not created:
            like.delete()
            return Response({'message': 'Like removed'}, status=200)
        return Response({'message': 'Liked'}, status=201)


class FavoriteProductView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        favorite, created = Favorite.objects.get_or_create(user=request.user, product=product)
        if not created:
            favorite.delete()
            return Response({'message': 'Removed from favorites'}, status=200)
        return Response({'message': 'Added to favorites'}, status=201)
