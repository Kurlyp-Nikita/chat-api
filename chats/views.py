from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from chats.models import Chat, Message


@csrf_exempt
def create_chat(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    title = request.POST.get('title', '').strip()  # ТЗ: пробелы по краям триммить

    # ТЗ: не пустой, длина 1..200
    if not title:
        return JsonResponse({'error': 'Title cannot be empty'}, status=400)
    if len(title) > 200:
        return JsonResponse({'error': 'Title too long (max 200 chars)'}, status=400)

    chat = Chat.objects.create(title=title)

    return JsonResponse({
        'id': chat.id,
        'title': chat.title,
        'created_at': chat.created_at.isoformat()
    }, status=201)


@csrf_exempt
def create_message(request, chat_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    chat = get_object_or_404(Chat, id=chat_id)  # ТЗ: 404 если чат не существует
    text = request.POST.get('text', '').strip()

    # не пустой
    if not text:
        return JsonResponse({'error': 'Text cannot be empty'}, status=400)

    # длина 1..5000
    if len(text) > 5000:
        return JsonResponse({'error': 'Text too long (max 5000 chars)'}, status=400)

    message = Message.objects.create(chat=chat, text=text)

    return JsonResponse({
        'id': message.id,
        'chat_id': message.chat.id,
        'text': message.text,
        'created_at': message.created_at.isoformat()
    }, status=201)


@csrf_exempt
def get_chat(request, chat_id):
    if request.method != 'GET':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    chat = get_object_or_404(Chat, id=chat_id)

    # limit по умолчанию 20
    try:
        limit = int(request.GET.get('limit', 20))
    except ValueError:
        limit = 20

    # максимум 100
    if limit > 100:
        limit = 100

    messages = chat.messages.order_by('-created_at')[:limit]

    return JsonResponse({
        'id': chat.id,
        'title': chat.title,
        'created_at': chat.created_at.isoformat(),
        'messages': [
            {
                'id': m.id,
                'text': m.text,
                'created_at': m.created_at.isoformat()
            }
            for m in messages
        ]
    })


@csrf_exempt
def delete_chat(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    chat.delete()

    return JsonResponse({}, status=204)