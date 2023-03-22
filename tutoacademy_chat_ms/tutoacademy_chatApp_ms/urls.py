from tutoacademy_chatApp_ms.views import chat_view 
from django.urls import path

urlpatterns = [
    path('chat/',chat_view.chatApi),
    path('chat/<int:id>/',chat_view.chatApiId),
    path('chat/<str:name>/',chat_view.chatApiUser)
]
