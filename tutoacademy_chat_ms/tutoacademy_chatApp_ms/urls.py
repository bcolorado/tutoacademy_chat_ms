from tutoacademy_chatApp_ms import views 
from django.urls import path

urlpatterns = [
    path('chat/',views.chatApi),
    #path('chat/<int:id>/',views.chatApi)
]
