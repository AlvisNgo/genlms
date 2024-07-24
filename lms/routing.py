from django.urls import path , include
from lms.views.consumer import ChatConsumer

websocket_urlpatterns = [
    path('<str:userid>', ChatConsumer.as_asgi()),
] 