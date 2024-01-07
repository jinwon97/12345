from .models import *
from .serializers import *

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework import generics

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

from urllib.parse import unquote
    
    
class SuggestionListView(generics.ListAPIView):
    def get_queryset(self):
        suggestion_contents = Suggestions.objects.values(
            'suggestion_id',
            'title',
            'creationdate',
            'user__username',
        )
        
        queryset = suggestion_contents
        return queryset
    
    serializer_class = SuggestionListSerializer
    
class SuggestionView(generics.ListAPIView):
    
    def get_queryset(self):

        suggestion_id = self.kwargs['pk']
        queryset = Suggestions.objects.filter(suggestion_id=suggestion_id).values(
            'suggestion_id',
            'title',
            'contents',
            'creationdate',
            'user__username',
        )
        
        return queryset

    serializer_class = SuggestionSerializer

class SuggestionSearchView(generics.ListAPIView):
    
    def get_queryset(self):
        if self.kwargs['searchfield'] == 'title':
            
            queryset = Suggestions.objects.filter(title__contains=unquote(self.kwargs['searchkeyword'])).values(
                'suggestion_id',
                'title',
                'creationdate',
                'user__username',
            )
            
        elif self.kwargs['searchfield'] == 'contents':
            
            queryset = Suggestions.objects.filter(contents__contains=unquote(self.kwargs['searchkeyword'])).values(
                'suggestion_id',
                'title',
                'creationdate',
                'user__username',
            )
            
        elif self.kwargs['searchfield'] == 'name':
            
            queryset = Suggestions.objects.filter(user__username__contain=unquote(self.kwargs['searchkeyword'])).values(
                'suggestion_id',
                'title',
                'creationdate',
                'user__username',
            )
            
        else:
            raise ValidationError({'error':'search field error'}, status.HTTP_404_NOT_FOUND)
        
        return queryset

    serializer_class = SuggestionSearchSerializer
@method_decorator(csrf_protect, name='dispatch')
class SuggestionCreateView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = SuggestionCreateSerializer
        
    def perform_create(self, serializer):
        
        Suggestions.objects.create(
            title=serializer.validated_data['title'],
            contents=serializer.validated_data['contents'],
            admin=self.request.user
        )
        
@method_decorator(csrf_protect, name='dispatch')
class SuggestionUpdateView(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = SuggestionUpdateSerializer
    queryset = Suggestions.objects.all()
    
    def perform_update(self, serializer):    
        instance = self.get_object()

        if instance.user != self.request.user : raise ValidationError({'error':'not the user'}, status.HTTP_403_FORBIDDEN)
        
        instance.title = serializer.validated_data['title']
        instance.tag = serializer.validated_data['tag']
        instance.contents = serializer.validated_data['contents']

        instance.save()
        
        
        
@method_decorator(csrf_protect, name='dispatch')
class SuggestionDeleteView(generics.DestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Suggestions.objects.all()
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        
        if instance.user != self.request.user :  raise ValidationError({'error':'not the user'}, status.HTTP_403_FORBIDDEN)
        
        instance.delete()
    
        return Response({'success' : 'delete announcement success'}, status.HTTP_200_OK)