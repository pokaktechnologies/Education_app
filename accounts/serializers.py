from rest_framework import serializers
from .models import User, OTP, Subject,Chapter, Topic, Note, RelatedTopic, Subscription
import random


class OTPSerializer(serializers.Serializer):
    otp = serializers.IntegerField()
    def validate(self, value):
        return value

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, data):
        return data
    
class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name', 'standard']

class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = ['id', 'name', 'subject']


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['id', 'content', 'created_at']  # Specify fields to be serialized

class RelatedTopicSerializer(serializers.ModelSerializer):
    related_topic = serializers.StringRelatedField()  # This will show the title of the related topic

    class Meta:
        model = RelatedTopic
        fields = ['related_topic']  # Only the related topic title

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['id', 'user', 'topic', 'subscribed_at']  # Specify fields to be serialized

class TopicSerializer(serializers.ModelSerializer):
    chapters = ChapterSerializer(many=True, read_only=True)
    notes = NoteSerializer(many=True, read_only=True)
    related_topics = RelatedTopicSerializer(many=True, read_only=True)

    class Meta:
        model = Topic
        fields = ['id', 'title', 'description', 'is_favourite', 'chapters', 'notes', 'related_topics']  # Specify fields to be serialized
