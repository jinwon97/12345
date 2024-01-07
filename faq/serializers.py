from rest_framework import serializers
from .models import *
        
class FaqListSerializer(serializers.Serializer):
    faq_id = serializers.IntegerField()
    title = serializers.CharField()
    date = serializers.DateTimeField()
    name = serializers.IntegerField()
    
    def to_representation(self, instance):
        return {
            'faq_id': instance['faq_id'],
            'title': instance['title'],
            'date': instance['creationdate'],
            'name': instance['admin__username']
        }

class FaqSerializer(serializers.Serializer):
    faq_id = serializers.IntegerField()
    title = serializers.CharField()
    contents = serializers.CharField()
    date = serializers.DateTimeField()
    name = serializers.IntegerField()
    
    def to_representation(self, instance):
        return {
            'faq_id': instance['faq_id'],
            'title': instance['title'],
            'contents': instance['contents'],
            'date': instance['creationdate'],
            'name': instance['admin__username']
        }
class FaqSearchSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        return {
            'faq_id': instance['faq_id'],
            'title': instance['title'],
            'date': instance['creationdate'],
            'name': instance['admin__username']
        }
    class Meta:
        model = Faq
        fields = ['faq_id', 'title', 'creationdate', 'admin__username']

class FaqCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Faq
        fields = ('title', 'contents')
class FaqUpdateSerializer(serializers.Serializer):

    title = serializers.CharField(required=False, allow_blank=True, allow_null=True, max_length=50)
    contents = serializers.CharField(required=False, allow_blank=True, allow_null=True, max_length=45)
    
    class Meta:
        model = Faq
        fields = ('title', 'contents')