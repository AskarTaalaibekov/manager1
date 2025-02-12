from django.urls import path
from .views import user_list, edit_user, change_status

urlpatterns = [
    path('', user_list, name='user_list'),
    path('edit/<int:user_id>/', edit_user, name='edit_user'),
    path('status/<int:user_id>/<str:status>/', change_status, name='change_status'),
]