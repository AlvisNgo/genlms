from .models import Notification
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
from datetime import datetime, timedelta
from django.conf import settings

def add_notification(to: int, title: str, description: str, link: str):
    notification = Notification(
        to=to,
        title=title,
        description=description,
        link=link
    )
    notification.save()
    
    return notification

def generate_sas_url(blob_name):
    blob_service_client = BlobServiceClient.from_connection_string(settings.AZURE_CONNECTION_STRING)
    blob_client = blob_service_client.get_blob_client(container=settings.AZURE_CONTAINER, blob=blob_name)

    sas_token = generate_blob_sas(
        account_name=settings.AZURE_ACCOUNT_NAME,
        container_name=settings.AZURE_CONTAINER,
        blob_name=blob_name,
        account_key=settings.AZURE_ACCOUNT_KEY,
        permission=BlobSasPermissions(read=True),
        expiry=datetime.utcnow() + timedelta(hours=1)  # Token valid for 1 hour
    )

    return f'{blob_client.url}?{sas_token}'
