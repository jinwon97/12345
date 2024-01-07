from rest_framework import serializers
from .models import BoardReview, CommentsReview
        
class BoardPostListSerializer(serializers.Serializer):
    post_id = serializers.IntegerField()
    title = serializers.CharField()

    date = serializers.DateTimeField()
    name = serializers.CharField()
    
    def to_representation(self, instance):
        return {
            'post_id': instance['board_id'],
            'title': instance['title'],
            'date': instance['creationdate'],
            'name': instance['user__name']
        }

class BoardPostSerializer(serializers.Serializer):
    post_id = serializers.IntegerField()
    title = serializers.CharField()
    contents = serializers.CharField()
    date = serializers.DateTimeField()
    name = serializers.CharField()
    
    def to_representation(self, instance):
        return {
            'post_id': instance['board_id'],
            'title': instance['title'],
            'contents': instance['contents'],
            'date': instance['creationdate'],
            'name': instance['user__name']
        }
        
class BoardPostCommentSerializer(serializers.Serializer):

    def to_representation(self, instance):
        return {
            'contents': instance['contents'],
            'date': instance['creationdate'],
            'name': instance['user__name'],
            'comment_id': instance['comment_id']
        }

class BoardSearchSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        return {
            'post_id': instance['board_id'],
            'title': instance['title'],
            'date': instance['creationdate'],
            'name': instance['user__name']
        }
    class Meta:
        model = BoardReview
        fields = ['post_id', 'title', 'creationdate', 'user__name']

class BoardPostCreateSerializer(serializers.ModelSerializer):

    title = serializers.CharField()
    contents = serializers.CharField()
    name = serializers.CharField()
    
    class Meta:
        model = BoardReview
        fields = ('title', 'contents', 'name')

class BoardPostUpdateSerializer(serializers.Serializer):

    title = serializers.CharField()
    contents = serializers.CharField()

        
class BoardPostcommentCreateSerializer(serializers.ModelSerializer):

    contents = serializers.CharField()
    name = serializers.CharField()
    
    class Meta:
        model = CommentsReview
        fields = ('contents', 'name')


class BoardPostCommentUpdateSerializer(serializers.ModelSerializer):

    contents = serializers.CharField()
    
    class Meta:
        model = CommentsReview
        fields = ('contents',)