from django.shortcuts import render
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect

from urllib.parse import unquote

from .models import *
from .serializers import *

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView

from .serializers import *

#******************************************************************************************************************************************************************
# 게시글 기능
#******************************************************************************************************************************************************************


class BoardPostListView(generics.ListAPIView):
    def get_queryset(self):
        board_contents = BoardConsult.objects.values(
            'board_id',
            'title',
            'creationdate',
            'user__username',
        )
        
        queryset = board_contents
        return queryset
    
    serializer_class = BoardPostListSerializer
    
class BoardPostView(generics.ListAPIView):
    
    def get_queryset(self):

        board_id = self.kwargs['pk']
        queryset = BoardConsult.objects.filter(board_id=board_id).values(
            'board_id',
            'title',
            'contents',
            'creationdate',
            'user__username',
        )
        
        return queryset

    serializer_class = BoardPostSerializer

class BoardSearchView(generics.ListAPIView):
    
    def get_queryset(self):
        if self.kwargs['searchfield'] == 'title':
            
            queryset = BoardConsult.objects.filter(title__contains=unquote(self.kwargs['searchkeyword'])).values(
                'board_id',
                'title',
                'creationdate',
                'user__username',
            )
            
        elif self.kwargs['searchfield'] == 'contents':
            
            queryset = BoardConsult.objects.filter(contents__contains=unquote(self.kwargs['searchkeyword'])).values(
                'board_id',
                'title',
                'creationdate',
                'user__username',
            )
            
        elif self.kwargs['searchfield'] == 'name':
            
            queryset = BoardConsult.objects.filter(user__username__contains=unquote(self.kwargs['searchkeyword'])).values(
                'board_id',
                'title',
                'creationdate',
                'user__username',
            )
            
        else:
            return HttpResponse("ERROR")
        
        
        return queryset

    serializer_class = BoardSearchSerializer
    
    
    
@method_decorator(csrf_protect, name='dispatch')
class BoardPostCreateView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = BoardPostCreateSerializer
        
    def perform_create(self, serializer):
        
        BoardConsult.objects.create(
            title=serializer.validated_data['title'],
            contents=serializer.validated_data['contents'],
            user=self.request.user
        )
        
        
        
@method_decorator(csrf_protect, name='dispatch')
class BoardPostUpdateView(generics.UpdateAPIView):#PATCH method
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = BoardPostUpdateSerializer
    queryset = BoardConsult.objects.all()
    
    def perform_update(self, serializer):                
        instance = self.get_object() # 입력(pk) 값으로 필터링해 대상 설정. 기본 대상은 테이블의 PK. 두 개 이상 또는 PK말고 다른 걸로 할 시 get_object 함수를 오버라이딩해야함.
        
        if instance.user != self.request.user: raise ValidationError({'error':'wrong user error'}, status.HTTP_403_FORBIDDEN)
        
        instance.title = serializer.validated_data['title']
        instance.contents = serializer.validated_data['contents']
        instance.save()

        return Response({'success':'create post success'}, status.HTTP_201_CREATED)
    
    
    
@method_decorator(csrf_protect, name='dispatch')
class BoardPostDeleteView(generics.DestroyAPIView):
    queryset = BoardConsult.objects.all()
    serializer_class = BoardPostSerializer
    
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        
        if instance.user != self.request.user:  raise ValidationError({'error':'wrong user error'})
        
        instance.delete()
        
        return Response({'success':'delte success'})
    
@method_decorator(csrf_protect, name='dispatch')
class BoardPostDeleteView(generics.DestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = BoardPostSerializer
    queryset = BoardConsult.objects.all()
    
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        
        if instance.user != self.request.user:  raise ValidationError({'error':'wrong user error'}, status.HTTP_401_UNAUTHORIZED)
        
        instance.delete()
        
        return Response({'success':'delete success'}, status.HTTP_200_OK)

#******************************************************************************************************************************************************************
# 댓글 기능
#******************************************************************************************************************************************************************

class BoardPostCommentView(generics.ListAPIView):
    
    def get_queryset(self):

        board_id = self.kwargs['pk']
        queryset = CommentsConsult.objects.filter(board=board_id).values(
            'contents',
            'creationdate',
            'user__username',
            'comment_id',
        )
        
        return queryset

    serializer_class = BoardPostCommentSerializer
    
    
    
@method_decorator(csrf_protect, name='dispatch')
class BoardPostCommentCreateView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = BoardPostcommentCreateSerializer
        
    def perform_create(self, serializer):
        board_id = BoardConsult.objects.get(board_id=self.kwargs['pk'])
        
        CommentsConsult.objects.create(
            contents=serializer.validated_data['contents'],
            user=self.request.user,
            board=board_id,
        )



@method_decorator(csrf_protect, name='dispatch')
class BoardPostCommentUpdateView(generics.UpdateAPIView):#PATCH method
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = BoardPostCommentUpdateSerializer
    queryset = CommentsConsult.objects.all()
    
    def perform_update(self, serializer):
        instance = self.get_object()
        
        if instance.user != self.request.user: raise ValidationError({'error':'wrong user error'}, status.HTTP_401_UNAUTHORIZED)
        instance.contents = serializer.validated_data['contents']
        instance.save()
        return Response({'success' : 'update comment success'}, status.HTTP_200_OK)
    
    
@method_decorator(csrf_protect, name='dispatch')
class BoardPostCommentDeleteView(generics.DestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = CommentsConsult.objects.all()
    
    def delete(self, reqeust, *args, **kwags):
        instance = self.get_object()
        
        if instance.user != self.request.user: raise ValidationError({'error':'wrong user error'}, status.HTTP_403_FORBIDDEN)
        
        instance.delete()
        return Response({'success' : 'delete comment success'}, status.HTTP_200_OK)
    


