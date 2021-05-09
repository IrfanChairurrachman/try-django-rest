from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from collections import OrderedDict
from .dump import *

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET', 'POST'])
def snippet_list(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        # print(serializer.data)
        
        test = get_popular()
        print(type(test))
        print(type(snippets))
        print(type(serializer.data))
        # print(test)
        # print(serializer.data)
        # content = JsonResponse(test, safe=False)
        # print(content)
        # return JsonResponse(serializer.data, safe=False)
        # return content
        # return Response(test)
        return Response(serializer.data)

    elif request.method == 'POST':
        # data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=request.data)
        # print(request)
        print(request.data['budget'])

        # if serializer.is_valid():
        #     # print(serializer.data)
        #     serializer.save()
        #     # return JsonResponse(serializer.data, status=201)
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # # return JsonResponse(serializer.data, status=201)
        # # return JsonResponse(serializer.errors, status=400)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse(request.data, safe=False)

@api_view(['GET', 'PUT', 'DELETE'])
def snippet_detail(request, pk, format=None):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)