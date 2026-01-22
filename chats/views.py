from django.http import JsonResponse
from django.shortcuts import render
from chats.models import Message, Chat


def create_chat(request):
    title = request.POST.get('title')

    if not title:
        return JsonResponse({'error': 'Title cannot be empty'}, status=400)

    chat = Chat.objects.create(title=title)

    return JsonResponse({
        'id': chat.id,
        'title': chat.title,
        'created_at': chat.created_at.isoformat()
    }, status=201)