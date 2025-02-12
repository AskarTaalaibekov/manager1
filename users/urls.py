from django.urls import path
from .views import user_list, edit_user, delete_user, add_user
from .views import schedule_interview,send_whatsapp_message
urlpatterns = [
    path('', user_list, name='user_list'),
    path('edit/<int:user_id>/', edit_user, name='edit_user'),
    path('delete/<int:user_id>/', delete_user, name='delete_user'),
    path('add/', add_user, name='add_user'),
    path('schedule/', schedule_interview, name='schedule_interview'),
    path('send_whatsapp/<str:whatsapp_number>/<str:mentor>/<str:date_time>/', send_whatsapp_message, name='send_whatsapp_message'),
]


