from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from tutoacademy_chatApp_ms.serializers import *
from django.utils import timezone


@csrf_exempt
def chatApi(request):

    # Get method that returns every chat in the DB
    if request.method == 'GET':
        chats = Chat.objects.all()
        chats_Serializer = ChatSerializer(chats, many=True)
        return JsonResponse(chats_Serializer.data, safe=False)


    # Post method that registers a new chat
    elif request.method == 'POST':
        chatsData = JSONParser().parse(request)
        chatsData["messages"][0]['sendTime'] = timezone.now()
        senderQuery = chatsData['sender']
        ReceiverQuery = chatsData['receiver']
        chatExist = Chat.objects.filter(sender=senderQuery, receiver=ReceiverQuery).values(
        ) | Chat.objects.filter(sender=ReceiverQuery, receiver=senderQuery).values()
        chatsData["messages"][0]['messageId'] = 1
        chats_Serializer = ChatSerializer(data=chatsData)

        if chats_Serializer.is_valid():
            if (chatExist):
                return JsonResponse('Chat beetwen these users already exist, please use patch', safe=False)
            
            else:
                chats_Serializer.save()
            return JsonResponse('Chat added succesfully', safe=False)
        
        return JsonResponse('Chat failed to add', safe=False)


    # PATCH method use to register new messages from an extinting chat
    elif request.method == "PATCH":
        chatsData = JSONParser().parse(request)
        senderQuery = chatsData['sender']
        ReceiverQuery = chatsData['receiver']
        chatExist = Chat.objects.filter(sender=senderQuery, receiver=ReceiverQuery).values(
        ) | Chat.objects.filter(sender=ReceiverQuery, receiver=senderQuery).values()
        chatsData["messages"][0]['sendTime'] = timezone.now()
        chatsData["messages"][0]['messageId'] = len(chatExist[0]['messages'])+1
        messages = chatsData["messages"]

        if not chatExist:
            return JsonResponse('There is no chat for those users, please use post to create it', safe=False)
        
        chatId1 = chatExist[0]["chatId"]
        chat = Chat.objects.get(chatId=chatId1)

        if chat is not None:
            chat.messages.extend(messages)
            chat.save()
            return JsonResponse('Added succesfully', safe=False)
        
        return JsonResponse('Failed to add', safe=False)
    
    else:
        return JsonResponse('There is no function for that request, please use GET/POST/PATCH', safe=False)
    
