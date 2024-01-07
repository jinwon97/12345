from django.shortcuts import render
from django.http import HttpResponse

from rest_framework import generics

from .models import *
from .serializers import *
    
class BoardPostListView(generics.ListAPIView):
    def get_queryset(self):
        board_contents = BoardReview.objects.values(
            'board_id',
            'title',
            'creationdate',
            'user__name',
        )
        
        queryset = board_contents
        return queryset
    
    serializer_class = BoardPostListSerializer
    
class BoardPostView(generics.ListAPIView):
    
    def get_queryset(self):

        board_id = self.kwargs['pk']
        queryset = BoardReview.objects.filter(board_id=board_id).values(
            'board_id',
            'title',
            'contents',
            'creationdate',
            'user__name',
        )
        
        return queryset

    serializer_class = BoardPostSerializer

class BoardPostCommentView(generics.ListAPIView):
    
    def get_queryset(self):

        board_id = self.kwargs['pk']
        queryset = CommentsReview.objects.filter(board=board_id).values(
            'contents',
            'creationdate',
            'user__name',
            'comment_id',
        )
        
        return queryset

    serializer_class = BoardPostCommentSerializer

class BoardSearchView(generics.ListAPIView):
    
    def get_queryset(self):
        board_id = self.kwargs['searchfield']
        if self.kwargs['searchfield'] == 'title':
            
            queryset = BoardReview.objects.filter(title__contains=self.kwargs['searchkeyword']).values(
                'board_id',
                'title',
                'creationdate',
                'user__name',
            )
            
        elif self.kwargs['searchfield'] == 'contents':
            
            queryset = BoardReview.objects.filter(contents__contains=self.kwargs['searchkeyword']).values(
                'board_id',
                'title',
                'creationdate',
                'user__name',
            )
            
        elif self.kwargs['searchfield'] == 'name':
            
            queryset = BoardReview.objects.filter(user__name__contains=self.kwargs['searchkeyword']).values(
                'board_id',
                'title',
                'creationdate',
                'user__name',
            )
            
        else:
            return HttpResponse("ERROR")
        
        
        print(queryset)
        return queryset

    serializer_class = BoardSearchSerializer

class BoardPostCreateView(generics.CreateAPIView):
    serializer_class = BoardPostCreateSerializer
        
    def perform_create(self, serializer):
        user_instance = User.objects.get(name=serializer.validated_data.get('name', ''))
        
        BoardReview.objects.create(
            title=serializer.validated_data['title'],
            contents=serializer.validated_data['contents'],
            user=user_instance
        )
        
class BoardPostUpdateView(generics.UpdateAPIView):#PATCH method
    serializer_class = BoardPostUpdateSerializer
    queryset = BoardReview.objects.all()
    def perform_update(self, serializer):    
        instance = self.get_object() # 입력(pk) 값으로 필터링해 대상 설정. 기본 대상은 테이블의 PK. 두 개 이상 또는 PK말고 다른 걸로 할 시 get_object 함수를 오버라이딩해야함.

        instance.title = serializer.validated_data['title']
        instance.contents = serializer.validated_data['contents']

        instance.save()

class BoardPostDeleteView(generics.DestroyAPIView):
    queryset = BoardReview.objects.all()
    serializer_class = BoardPostSerializer
    

#******************************************************************************************************************************************************************
# 댓글 기능
#******************************************************************************************************************************************************************
class BoardPostCommentCreateView(generics.CreateAPIView):

    serializer_class = BoardPostcommentCreateSerializer
        
    def perform_create(self, serializer):
        user_instance = User.objects.get(name=serializer.validated_data.get('name', ''))
        board_id = BoardReview.objects.get(board_id=self.kwargs['pk'])
        
        CommentsReview.objects.create(
            contents=serializer.validated_data['contents'],
            user=user_instance,
            board=board_id,
        )

class BoardPostCommentUpdateView(generics.UpdateAPIView):#PATCH method
    serializer_class = BoardPostCommentUpdateSerializer
    
    queryset = CommentsReview.objects.all()
    
    def perform_update(self, serializer):    
        instance = self.get_object()

        instance.contents = serializer.validated_data['contents']

        instance.save()

class BoardPostDeleteView(generics.DestroyAPIView):
    queryset = BoardReview.objects.all()
    serializer_class = BoardPostSerializer