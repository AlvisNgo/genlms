from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='admin_index'),
    path('import_valid_rows/', views.import_valid_rows, name='import_valid_rows'),
]