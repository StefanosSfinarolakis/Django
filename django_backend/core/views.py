from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Image
from .serializers import ImageSerializer

@api_view(['POST'])
def image_upload_view(request):
    serializer = ImageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
def image_list_view(request):
    images = Image.objects.all()
    serializer = ImageSerializer(images, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def image_detail_view(request, pk):
    image = Image.objects.get(pk=pk)
    serializer = ImageSerializer(image)
    return Response(serializer.data)