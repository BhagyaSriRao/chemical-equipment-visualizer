from django.urls import path
from .views import upload_csv, upload_history, download_pdf

urlpatterns = [
    path('upload/', upload_csv),
    path('history/', upload_history),
    path('download-pdf/', download_pdf),
]
