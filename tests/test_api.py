# from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

from apps.messageapp.models import Message
from apps.messageapp.views import MessageConfirmApiView
from core.settings import NEW_MESSAGE_URL, MESSAGE_CONFIRM_URL, DEFAULT_USER


class MessageApiTestCase(APITestCase):

    def test_post_message(self):
        """
        Ensure we create a new message.
        {
        "user_id": 2022,
        "message": "Для современного мира разбавленное изрядной  эмпатии, рациональное мышление выявляет "
        }
        http://127.0.0.1:8000/api/v1/message/
        """

        data = {"user_id": 1235, "message": "text"}

        url = reverse('message_detail')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Message.objects.count(), 1)
        self.assertEqual(Message.objects.get().message, data.get('message'))

    def test_api_message(self):
        """
        Ensure we create a new message.
        {
        "user_id": 2022,
        "message": "Для современного мира разбавленное изрядной  эмпатии, рациональное мышление выявляет "
        }
        http://127.0.0.1:8000/api/v1/message/
        """

        data = {"user_id": 123, "message": "text"}

        url = NEW_MESSAGE_URL
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Message.objects.count(), 1)
        self.assertEqual(Message.objects.get().message, data.get('message'))

    def test_post_message_confirmation(self):
        """
        {
        "message_id": 6,
        "success": false
        }

        http://127.0.0.1:8000/api/v1/message_confirmation/
        """
        message1 = Message.objects.create(user_id=123, message="text")

        if MessageConfirmApiView.permission_classes == [IsAuthenticated]:
            # username = "TestUser"
            # user1 = User.objects.create_user(username=username, password="Aa123456789bB")
            # self.client.force_authenticate(user=user1)

            # Djoser:
            self.user = self.client.post('/register/users/', data=DEFAULT_USER)

            # Token:
            # response = self.client.post('/auth/token/login/', data=user_data)
            # self.token = response.data['auth_token']
            # self.client.credentials(HTTP_AUTHORIZATION='Token '+self.token)

            # JWT:
            response = self.client.post('/jwt/token/', data=DEFAULT_USER)
            print(f"{response=}")
            self.token = response.data['access']
            self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        params = {
            "message_id": message1.pk,
            "success": True
        }
        url = MESSAGE_CONFIRM_URL

        response = self.client.post(url, params, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Message.objects.count(), 1)
        self.assertEqual(Message.objects.get().pk, params.get('message_id'))
