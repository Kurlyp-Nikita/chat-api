from django.http import JsonResponse
from django.shortcuts import render
from chats.models import Message, Chat
from django.shortcuts import get_object_or_404


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


def create_message(request, chat_id):

    chat = get_object_or_404(Chat, id=chat_id)
    text = request.POST.get('text', '').strip()

    if not text:
        return JsonResponse({'error': 'Text cannot be empty'}, status=400)

    message = Message.objects.create(chat=chat, text=text)

    return JsonResponse({
        'id': message.id,
        'chat_id': message.chat.id,
        'text': message.text,
        'created_at': message.created_at.isoformat()
    })


def get_chat(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)

    limit = int(request.GET.get("limit", 20))
    if limit > 100:
        limit = 100

    # Последние сообщения сначала
    messages = chat.messages.order_by("-created_at")[:limit]

    return JsonResponse({
        "id": chat.id,
        "title": chat.title,
        "created_at": chat.created_at.isoformat(),
        "messages": [
            {
                "id": m.id,
                "text": m.text,
                "created_at": m.created_at.isoformat(),
            }
            for m in messages
        ]
    })



