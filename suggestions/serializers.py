from rest_framework import serializers
from .models import Suggestions, user

class SuggestionListSerializer(serializers.Serializer):
    post_id = serializers.IntegerField()
    title = serializers.CharField()
    post_tag = serializers.CharField()
    date = serializers.DateTimeField()
    name = serializers.CharField()
    
    def to_representation(self, instance):
        return {
            'suggestion_id': instance['suggestion_id'],
            'title': instance['title'],
            'date': instance['creationdate'],
            'name': instance['user__name']
        }

class SuggestionSerializer(serializers.Serializer):
    post_id = serializers.IntegerField()
    title = serializers.CharField()
    tag = serializers.CharField()
    contents = serializers.CharField()
    date = serializers.DateTimeField()
    name = serializers.CharField()
    
    def to_representation(self, instance):
        return {
            'suggestion_id': instance['suggestion_id'],
            'title': instance['title'],
            'contents': instance['contents'],
            'date': instance['creationdate'],
            'name': instance['user__name']
        }

class SuggestionSearchSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        return {
            'suggestion_id': instance['suggestion_id'],
            'title': instance['title'],
            'date': instance['creationdate'],
            'name': instance['user__name']
        }
    class Meta:
        model = Suggestions
        fields = ['suggestion_id', 'title', 'tag', 'creationdate', 'user__name']

class SuggestionCreateSerializer(serializers.ModelSerializer):

    title = serializers.CharField()
    contents = serializers.CharField()
    name = serializers.CharField()
    
    class Meta:
        model = Suggestions
        fields = ('title', 'contents', 'name')

class SuggestionUpdateSerializer(serializers.Serializer):

    title = serializers.CharField()
    contents = serializers.CharField()
