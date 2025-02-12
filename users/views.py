from django.shortcuts import render, get_object_or_404, redirect
from .models import UserProfile,Interview
from .forms import UserForm,InterviewForm
import urllib.parse
from datetime import datetime



def user_list(request):
    query = request.GET.get('q')
    status_filter = request.GET.get('status')
    direction_filter = request.GET.get('direction')

    users = UserProfile.objects.all()

    if query:
        users = users.filter(name__icontains=query) | users.filter(phone__icontains=query)

    if status_filter:
        users = users.filter(status=status_filter)
    if direction_filter:
        users = users.filter(direction=direction_filter)

    return render(request, 'users/user_list.html', {'users': users})

def edit_user(request, user_id):
    user = get_object_or_404(UserProfile, id=user_id)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserForm(instance=user)
    return render(request, 'users/edit_user.html', {'form': form, 'user': user})

def delete_user(request, user_id):
    user = get_object_or_404(UserProfile, id=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('user_list')
    return render(request, 'users/delete_user.html', {'user': user})

def add_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserForm()
    return render(request, 'users/add_user.html', {'form': form})

def schedule_interview(request):
    if request.method == "POST":
        form = InterviewForm(request.POST)
        if form.is_valid():
            interview = form.save()
            formatted_date = interview.date_time.strftime("%Y-%m-%d %H:%M")
            return redirect('send_whatsapp_message', whatsapp_number=interview.whatsapp_number, mentor=interview.mentor, date_time=formatted_date)
    else:
        form = InterviewForm()
    return render(request, 'users/schedule_interview.html', {'form': form})

def send_whatsapp_message(request, whatsapp_number, mentor, date_time):
    try:
        # Туура форматка келтирүү
        parsed_date = datetime.strptime(date_time, "%Y-%m-%d %H:%M")
        formatted_date = parsed_date.strftime("%d-%m-%Y %H:%M")

        # WhatsApp үчүн билдирүү
        message = f"Сиз {formatted_date} убакытка {mentor} менен маектешүүгө чакырылдыңыз!"
        encoded_message = urllib.parse.quote(message)
        whatsapp_url = f"https://api.whatsapp.com/send?phone={whatsapp_number}&text={encoded_message}"
        return redirect(whatsapp_url)

    except Exception as e:
        return render(request, 'users/error.html', {'error': str(e)})