from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, SlugRelatedField

from .models import Message


class MessageListSerializer(ModelSerializer):
    """Сериалайзер списка сообщений"""
    class Meta:
        model = Message
        fields = '__all__'


class MessageSerializer(ModelSerializer):
    """Сериалайзер сообщения"""
    class Meta:
        model = Message
        fields = '__all__'


class MessageConfirmationSerializer(serializers.Serializer):
    """Сериалайзер подтверждения сообщения"""
    message_id = serializers.IntegerField()
    success = serializers.BooleanField(default=False)

    def create(self, validated_data):
        return Message(**validated_data)

    def update(self, instance, validated_data):
        MessageStatuses = Message.MessageStatuses
        instance.status = MessageStatuses.CORRECT if validated_data.get("success") else MessageStatuses.BLOCKED
        instance.time_update = validated_data.get("success")
        instance.save()
        return instance
