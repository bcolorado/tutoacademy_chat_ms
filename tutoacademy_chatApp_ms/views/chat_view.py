from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from tutoacademy_chatApp_ms.serializers.chat_serializer import *
from django.utils import timezone
from tutoacademy_chatApp_ms.queue.consumer import *

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

        #Search for a chat if exist between those two users
        chatExist = Chat.objects.filter(sender=senderQuery, receiver=ReceiverQuery).values(
        ) | Chat.objects.filter(sender=ReceiverQuery, receiver=senderQuery).values()

        if not chatExist:
            return JsonResponse('There is no chat for those users, please use post to create it', safe=False)
        
        #Add manually createDate and UniqueId
        chatsData["messages"][0]['sendTime'] = timezone.now()
        chatsData["messages"][0]['messageId'] = len(chatExist[0]['messages'])+1
        messages = chatsData["messages"]


        #Obtains the data from that specific chat
        chatId1 = chatExist[0]["chatId"]
        chat = Chat.objects.get(chatId=chatId1)

        if chat is not None:
            #Adds the new message to the list of messages in that chat
            chat.messages.extend(messages)
            chat.save()
            return JsonResponse('Added succesfully', safe=False)
        
        return JsonResponse('Failed to add', safe=False)
    
    else:
        return JsonResponse('There is no function for that request, please use GET/POST/PATCH', safe=False)
    


# Function that returns a chat with an ID given
@csrf_exempt
def chatApiId(request,id):
    try: 
        chat= Chat.objects.get(pk=id)
    except Chat.DoesNotExist:
        return JsonResponse('The chat does not exist, please create one with POST', safe=False)
    
    if request.method =='GET':
        chat_serializer= ChatSerializer(chat)
        return JsonResponse(chat_serializer.data, safe=False)
    
    else:
        return JsonResponse('There is no function for that request, please use GET/id/', safe=False)


 # Function that returns a chat with an User given
@csrf_exempt
def chatApiUser(request,name):

    chatsExist = Chat.objects.filter(sender=name).values(
    ) | Chat.objects.filter(receiver=name).values()

    if(len(chatsExist)==0):
        return JsonResponse('This user does not have any chat', safe=False)
    
    elif request.method =='GET':
        chats_serializer= ChatSerializer(chatsExist,many=True)
        return JsonResponse(chats_serializer.data, safe=False)
    
    else:
        return JsonResponse('There is no function for that request, please use GET/user/', safe=False)