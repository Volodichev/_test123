from django.db import transaction
from django.http import HttpResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListCreateAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.messageapp.models import Message
from apps.messageapp.serializers import MessageSerializer, MessageConfirmationSerializer, MessageListSerializer
from core.settings import KAFKA_TOPIC
from services.kafka_services import send_to_kafka


def homepageview(request):
    return HttpResponse('url example: http://127.0.0.1:8000/api/v1/message/')


class SomeError(Exception):
    pass


class MessageApiViewList(APIView):

    def get(self, request):
        messages = Message.objects.all()  # values()
        serializer = MessageListSerializer(messages, many=True)
        return Response({"Messages": serializer.data})


class MessageApiViewDetail(APIView):
    def get(self, request, pk):
        message = get_object_or_404(Message, pk=pk)
        serializer = MessageSerializer(data=message)
        return Response(serializer.data)

    def post(self, request):
        try:
            with transaction.atomic():
                message = request.data
                serializer = MessageSerializer(data=message)
                if serializer.is_valid(raise_exception=True):
                    message_saved = serializer.save()
                    print(f"{serializer=}")
                    message_id = serializer.data.get("id")
                    user_id = serializer.data.get("user_id")
                    message_text = serializer.data.get("message")
                    data = {"message_id": message_id, "user_id": user_id, "text": message_text}
                    send_to_kafka(data=data, topic_name=KAFKA_TOPIC)
                else:
                    raise SomeError()

                return Response({"success": "Message '{}' created successfully".format(message_saved.message)})

        except SomeError:
            pass

        return Response({"error something go wrong"})


class MessageConfirmApiView(APIView):
    """"""

    permission_classes = [IsAuthenticated]
    # authentication_classes = (TokenAuthentication,) #Для обычных токенов

    def post(self, request, *args, **kwargs):
        message_id = request.data.get("message_id", None)
        if not message_id:
            return Response({"reror": "Method PUT not allowded"})

        try:
            instance = Message.objects.get(pk=message_id)
        except:
            return Response({"reror": "object does not exist"})

        message = request.data
        serializer = MessageConfirmationSerializer(data=message, instance=instance)
        if serializer.is_valid(raise_exception=True):
            message_saved = serializer.save()

        return Response({"success": "ok"})
