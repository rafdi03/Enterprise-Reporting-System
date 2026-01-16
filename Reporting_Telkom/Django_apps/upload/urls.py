from django.urls import path
from . import views

urlpatterns = [
    path('', views.report_view, name='report_view'),
    path('upload/', views.upload_view, name='upload_home'),
    path('api/update_cell/', views.update_cell_api, name='update_cell'),
    path('download/<str:suffix>/<str:format_type>/', views.download_report, name='download_report'),
]