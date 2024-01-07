from django.shortcuts import render
from django.http import HttpResponse
from urllib.parse import unquote
from rest_framework import generics, status, permissions
from django.views.decorators.csrf import csrf_protect
from .models import *
from .serializers import *
from django.utils.decorators import method_decorator


from rest_framework import generics
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView

from .serializers import *
from account.models import UserCustom

#******************************************************************************************************************************************************************
# 게시글 기능
#******************************************************************************************************************************************************************
    


class BoardPostListView(generics.ListAPIView):
    
    def get_queryset(self):
        board_contents = Board.objects.values(
            'board_id',
            'title',
            'creationdate',
            'user__username',
        )
        
        queryset = board_contents
        return queryset
    
    serializer_class = BoardPostListSerializer



class BoardPostView(generics.ListAPIView):
    #permission_classes = (permissions.AllowAny,)
    def get_queryset(self):

        board_id = self.kwargs['pk']
        queryset = Board.objects.filter(board_id=board_id).values(
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
            
            queryset = Board.objects.filter(title__contains=unquote(self.kwargs['searchkeyword'])).values(
                'board_id',
                'title',
                'creationdate',
                'user__username',
            )
            
        elif self.kwargs['searchfield'] == 'contents':
            
            queryset = Board.objects.filter(contents__contains=unquote(self.kwargs['searchkeyword'])).values(
                'board_id',
                'title',
                'creationdate',
                'user__username',
            )
            
        elif self.kwargs['searchfield'] == 'username':
            
            queryset = Board.objects.filter(user__username__contains=unquote(self.kwargs['searchkeyword'])).values(
                'board_id',
                'title',
                'creationdate',
                'user__username',
            )
            
        else:
            return Response()
        
        
        return queryset

    serializer_class = BoardSearchSerializer
    
    
    
@method_decorator(csrf_protect, name='dispatch')
class BoardPostCreateView(generics.CreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = BoardPostCreateSerializer
        
    def perform_create(self, serializer):
    
        
        Board.objects.create(
            title=serializer.validated_data['title'],
            contents=serializer.validated_data['contents'],
            user=self.request.user
        )      
        return Response({'success': 'create post success'}, status.HTTP_201_CREATED)


@method_decorator(csrf_protect, name='dispatch')
class BoardPostUpdateView(generics.UpdateAPIView):#PATCH method
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = BoardPostUpdateSerializer
    queryset = Board.objects.all()
    
    def perform_update(self, serializer):
        if type(self.kwargs['pk']) != int or self.kwargs['pk'] < 1 : return Response({'error' : 'post number error'}, status = status.HTTP_404_NOT_FOUND)
            
        instance = self.get_object() # 입력(pk) 값으로 필터링해 대상 설정. 기본 대상은 테이블의 PK. 두 개 이상 또는 PK말고 다른 걸로 할 시 get_object 함수를 오버라이딩해야함.
        

        if instance.user != self.request.user:  raise ValidationError({'error':'wrong user error'}, status = status.HTTP_403_FORBIDDEN)
        
        else:
            instance.title = serializer.validated_data['title']
            instance.contents = serializer.validated_data['contents']

            instance.save()
        return Response({'success': 'update post success'}, status.HTTP_201_CREATED)
        

@method_decorator(csrf_protect, name='dispatch')
class BoardPostDeleteView(generics.DestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Board.objects.all()
    serializer_class = BoardPostSerializer
    
    def delete(self, request, *args, **kwargs):
        username = self.request.user.username
        instance = self.get_object()
        if instance.user != self.request.user:  
            return Response({'error':'wrong user error'}, status = status.HTTP_403_FORBIDDEN)
        else:
            instance.delete()
            
            return Response({'success':'delte success'}, status.HTTP_200_OK)
    

#******************************************************************************************************************************************************************
# 댓글 기능
#******************************************************************************************************************************************************************
class BoardPostCommentView(generics.ListAPIView):
    #permission_classes = (permissions.AllowAny,)
    def get_queryset(self):

        board_id = self.kwargs['pk']
        queryset = Comments.objects.filter(board=board_id).values(
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
        board_id = Board.objects.get(board_id=self.kwargs['pk'])
        
        Comments.objects.create(
            contents=serializer.validated_data['contents'],
            user=self.request.user,
            board=board_id,
        )
        return Response({'success': 'crate comment success'}, status.HTTP_201_CREATED)
@method_decorator(csrf_protect, name='dispatch')
class BoardPostCommentUpdateView(generics.UpdateAPIView):#PATCH method
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = BoardPostCommentUpdateSerializer
    queryset = Comments.objects.all()
    
    def perform_update(self, serializer):

        instance = self.get_object()
        
        if instance.user != self.request.user: raise ValidationError({'error':'wrong user error'}, status = status.HTTP_403_FORBIDDEN)
        
        instance.contents = serializer.validated_data['contents']

        instance.save()
@method_decorator(csrf_protect, name='dispatch')
class BoardPostCommentDeleteView(generics.DestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Comments.objects.all()
    
    def delete(self, request, *args, **kwargs):
    
        instance = self.get_object()
        if instance.user != self.request.user: raise ValidationError({'error':'wrong user error'}, status = status.HTTP_403_FORBIDDEN)
        
        instance.delete()
        return Response({'success':'delete success'}, status.HTTP_200_OK)