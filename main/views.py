from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404  
from .models import Product
from .serializers import ReviewSerializer, ProductListSerializer, ProductDetailsSerializer

@api_view(['GET'])
def products_list_view(request):
    products = Product.objects.all() 
    serializer = ProductListSerializer(products, many=True)  
    return Response(serializer.data) 

class ProductDetailsView(APIView):
    def get(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id) 
        except Product.DoesNotExist:
            raise Http404("Product not found") 
        
        serializer = ProductDetailsSerializer(product) 
        return Response(serializer.data)


class ProductFilteredReviews(APIView):
    def get(self, request, product_id):
        mark = request.query_params.get('mark', None)  
        try:
            product = Product.objects.get(id=product_id)  
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=404)  

        if mark is not None:
            reviews = product.reviews.filter(mark=mark) 
        else:
            reviews = product.reviews.all()  

        review_serializer = ReviewSerializer(reviews, many=True)  
        return Response(review_serializer.data)  
