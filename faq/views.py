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
#******************************************************************************************************************************************************************
# 게시글 기능
#******************************************************************************************************************************************************************
    
class FaqListView(generics.ListAPIView):
    def get_queryset(self):
        board_contents = Faq.objects.values(
            'faq_id',
            'title',
            'creationdate',
            'admin__username',
        )
        
        queryset = board_contents
        return queryset
    
    serializer_class = FaqListSerializer
    
class FaqView(generics.ListAPIView):
    
    def get_queryset(self):

        faq_id = self.kwargs['pk']
        queryset = Faq.objects.filter(faq_id=faq_id).values(
            'faq_id',
            'title',
            'contents',
            'creationdate',
            'admin__username',
        )
        
        return queryset

    serializer_class = FaqSerializer

class FaqSearchView(generics.ListAPIView):
    
    def get_queryset(self):
        if self.kwargs['searchfield'] == 'title':
            
            queryset = Faq.objects.filter(title__contains=unquote(self.kwargs['searchkeyword'])).values(
                'faq_id',
                'title',
                'creationdate',
                'admin__username',
            )
            
        elif self.kwargs['searchfield'] == 'contents':
            
            queryset = Faq.objects.filter(contents__contains=unquote(self.kwargs['searchkeyword'])).values(
                'faq_id',
                'title',
                'creationdate',
                'admin__username',
            )
            
        else:
            raise ValidationError({'error' : 'input error'}, status.HTTP_404_NOT_FOUND)
        
        return queryset

    serializer_class = FaqSearchSerializer
@method_decorator(csrf_protect, name='dispatch')
class FaqCreateView(generics.CreateAPIView):
    #permission_classes = (permissions.IsAdminUser,)
    serializer_class = FaqCreateSerializer
        
    def perform_create(self, serializer):
        
        Faq.objects.create(
            title=serializer.validated_data['title'],
            contents=serializer.validated_data['contents'],
            admin = self.request.user
        )
        

@method_decorator(csrf_protect, name='dispatch')
class FaqUpdateView(generics.UpdateAPIView):#PATCH method
    #permission_classes = (permissions.IsAdminUser,)
    serializer_class = FaqUpdateSerializer
    queryset = Faq.objects.all()
    
    def perform_update(self, serializer):    
        instance = self.get_object()
        
        if serializer.is_valid() != True : raise ValidationError({'error' : 'update announcement failed'}, status.HTTP_400_BAD_REQUEST)
        
        if 'title' in serializer.validated_data:
            
            if serializer.validated_data['title'] != '':
                instance.title = serializer.validated_data['title']
        
        if 'contents' in serializer.validated_data:
            
            if serializer.validated_data['contents'] != '':
                instance.contents = serializer.validated_data['contents']

        instance.save()
        
        return Response({'success':'update faq success'}, status.HTTP_200_OK)




@method_decorator(csrf_protect, name='dispatch')
class FaqDeleteView(generics.DestroyAPIView):
    #permission_classes = (permissions.IsAdminUser,)
    queryset = Faq.objects.all()
    serializer_class = FaqSerializer
    
    def delete(self, request, *args, **kwargs):
        
        instance = self.get_object()
        instance.delete()
        
        return Response({'success':'delete success'})