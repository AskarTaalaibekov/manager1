from django.urls import path
from .views import (
    user_list, edit_user, delete_user, add_user,
    schedule_interview, send_whatsapp_message,
    interview_list, toggle_theme,settings_view
)

urlpatterns = [
    path('', user_list, name='user_list'),
    path('edit/<int:user_id>/', edit_user, name='edit_user'),
    path('delete/<int:user_id>/', delete_user, name='delete_user'),
    path('add/', add_user, name='add_user'),
    path('schedule/', schedule_interview, name='schedule_interview'),
    path('interview_list/', interview_list, name='interview_list'),
    path('toggle_theme/', toggle_theme, name='toggle_theme'),  # Тема алмаштыруу
    path('send_whatsapp/<str:whatsapp_number>/<str:mentor>/<path:date_time>/<str:user_name>/',
         send_whatsapp_message, name='send_whatsapp_message'),
    path('settings/', settings_view, name='settings'),
]
