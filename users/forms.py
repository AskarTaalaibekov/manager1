from django import forms
from .models import UserProfile,Interview


class UserForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name', 'phone','status', 'direction',]



MENTOR_CHOICES = [
    ('Эламан', 'Эламан'),
    ('Marlis', 'Marlis'),
    ('Akdil', 'Akdil'),
]

class InterviewForm(forms.ModelForm):
    mentor = forms.ChoiceField(choices=MENTOR_CHOICES, label="Ментор")
    date_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        label="Маектешүү убактысы"
    )
    whatsapp_number = forms.CharField(
        max_length=15,
        label="WhatsApp номер",
        widget=forms.TextInput(attrs={'placeholder': '+996 XXX XXX XXX'})
    )

    class Meta:
        model = Interview
        fields = ['user', 'mentor', 'date_time', 'whatsapp_number']