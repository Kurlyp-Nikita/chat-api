from django.test import TestCase
from django.urls import reverse
from chats.models import Chat, Message
import json


class ChatAPITests(TestCase):
    def setUp(self):
        self.chat = Chat.objects.create(title="Test Chat")

    def test_create_chat(self):
        url = reverse('create-chat')
        response = self.client.post(url, {'title': 'New Chat'})

        self.assertEqual(response.status_code, 201)
        data = json.loads(response.content)
        self.assertEqual(data['title'], 'New Chat')
        self.assertIn('id', data)

    def test_create_chat_empty_title(self):
        url = reverse('create-chat')
        response = self.client.post(url, {'title': ''})

        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertIn('error', data)

    def test_create_message(self):
        url = reverse('create-message', args=[self.chat.id])
        response = self.client.post(url, {'text': 'Hello World'})

        self.assertEqual(response.status_code, 201)
        data = json.loads(response.content)
        self.assertEqual(data['text'], 'Hello World')
        self.assertEqual(data['chat_id'], self.chat.id)

    def test_get_chat_with_messages(self):
        # Создаем сообщение
        Message.objects.create(chat=self.chat, text="Test message")

        url = reverse('get-chat', args=[self.chat.id])
        response = self.client.get(url, {'limit': 5})

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['id'], self.chat.id)
        self.assertEqual(len(data['messages']), 1)

    def test_delete_chat(self):
        url = reverse('delete-chat', args=[self.chat.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(Chat.objects.count(), 0)