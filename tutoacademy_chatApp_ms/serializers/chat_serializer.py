#Help to convert the complex types or model instances into native python data types that can easily rendered into JSON 
from rest_framework import serializers
from tutoacademy_chatApp_ms.models.chat_model import  Message,Chat



class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model=Message
        fields= ("messageId",'sender','body','sendTime')

class ChatSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True)
    class Meta:
        model=Chat
        fields= ('chatId','sender','receiver','messages','state','createTime')