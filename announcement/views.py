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
# 공지글 기능
#******************************************************************************************************************************************************************



class AnnouncementListView(generics.ListAPIView):

    def get_queryset(self):
        announcement_contents = Announcements.objects.values(
            'announcement_id',
            'creationdate',
            'title',
            'admin__username',
        )
        
        queryset = announcement_contents
        return queryset
    
    serializer_class = AnnouncementListSerializer
    
    
    
class AnnouncementView(generics.ListAPIView):

    def get_queryset(self):
        print(self.kwargs['pk'])
        announcement_id = self.kwargs['pk']
        
        queryset = Announcements.objects.filter(announcement_id=announcement_id).values(
            'announcement_id',
            'title',
            'contents',
            'creationdate',
            'admin__username',
        )
        return queryset

    serializer_class = AnnouncementSerializer
    
    

class AnnouncementSearchView(generics.ListAPIView):
    serializer_class = AnnouncementSearchSerializer
    
    def get_queryset(self):
        if self.kwargs['searchfield'] == 'title':

            queryset = Announcements.objects.filter(title__contains=unquote(self.kwargs['searchkeyword'])).values(
                'announcement_id',
                'title',
                'creationdate',
                'admin__username',
            )
            
        elif self.kwargs['searchfield'] == 'contents':
            
            queryset = Announcements.objects.filter(contents__contains=unquote(self.kwargs['searchkeyword'])).values(
                'announcement_id',
                'title',
                'creationdate',
                'admin__username',
            )
            
        elif self.kwargs['searchfield'] == 'admin':
            
            queryset = Announcements.objects.filter(user__username__contains=unquote(self.kwargs['searchkeyword'])).values(
                'announcement_id',
                'title',
                'creationdate',
                'admin__username',
            )
        else:
            raise ValidationError({'error':'search field error'}, status.HTTP_404_NOT_FOUND)
        return queryset
    
    

@method_decorator(csrf_protect, name='dispatch')
class AnnouncementCreateView(generics.CreateAPIView):
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = AnnouncementCreateSerializer
        
    def perform_create(self, serializer):
        
        Announcements.objects.create(
            title=serializer.validated_data['title'],
            contents=serializer.validated_data['contents'],
            admin=self.request.user
        )
        
        
        
@method_decorator(csrf_protect, name='dispatch')
class AnnouncementUpdateView(generics.UpdateAPIView):
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = AnnouncementUpdateSerializer
    queryset = Announcements.objects.all()
    
    def perform_update(self, request):    
        instance = self.get_object()
        
        serializer = self.serializer_class(data = self.request.data, partial = True)
        
        if serializer.is_valid() != True : raise ValidationError({'error' : 'update announcement failed'}, status.HTTP_400_BAD_REQUEST)
        
        if 'title' in serializer.validated_data:
            
            if serializer.validated_data['title'] != '':
                instance.title = serializer.validated_data['title']
        
        if 'contents' in serializer.validated_data:
            
            if serializer.validated_data['contents'] != '':
                instance.contents = serializer.validated_data['contents']

        instance.save()
        
        return Response({'success':'update announcement success'}, status.HTTP_200_OK)
    
    
    
@method_decorator(csrf_protect, name='dispatch')
class AnnouncementdeleteView(generics.DestroyAPIView):
    permission_classes = (permissions.IsAdminUser,)
    queryset = Announcements.objects.all()
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        
        instance.delete()
        
        return Response({'success' : 'delete announcement success'}, status.HTTP_200_OK)