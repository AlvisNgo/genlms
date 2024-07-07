from django.urls import path , include
from lms.views.consumer import ChatConsumer

websocket_urlpatterns = [
    path("" , ChatConsumer.as_asgi()) , 
] 