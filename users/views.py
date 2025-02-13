from django.shortcuts import render, get_object_or_404, redirect
from .models import UserProfile, Interview
from .forms import UserForm, InterviewForm
import urllib.parse
from datetime import datetime
# from django.http import HttpResponse
from django.urls import reverse

def user_list(request):
    """Издөө жана фильтрлер"""
    query = request.GET.get('q')
    status_filter = request.GET.get('status')
    direction_filter = request.GET.get('direction')

    users = UserProfile.objects.all()  # Бардык колдонуучуларды алуу

    if query:
        users = users.filter(name__icontains=query) | users.filter(phone__icontains=query)

    if status_filter:
        users = users.filter(status=status_filter)

    if direction_filter:
        users = users.filter(direction=direction_filter)

    return render(request, 'users/user_list.html', {'users': users})
# def user_list(request):
#     """Бардык колдонуучуларды издөө."""
#     query = request.GET.get('q')
#
#     users = UserProfile.objects.all()  # Бардык колдонуучуларды алуу
#
#     if query:
#         users = users.filter(name__icontains=query) | users.filter(phone__icontains=query)
#
#     return render(request, 'users/user_list.html', {'users': users})


def interview_list(request):
    """Чакырылган колдонуучуларды жана алардын чакырылган убактысын көрсөтүү."""
    invited_users = Interview.objects.select_related('user')
    return render(request, 'users/interview_list.html', {'users': invited_users})


def edit_user(request, user_id):
    """Колдонуучуну түзөтүү"""
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
    """Колдонуучуну өчүрүү"""
    user = get_object_or_404(UserProfile, id=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('user_list')
    return render(request, 'users/delete_user.html', {'user': user})


def add_user(request):
    """Жаңы колдонуучу кошуу"""
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserForm()
    return render(request, 'users/add_user.html', {'form': form})


def schedule_interview(request):
    """Колдонуучуну маектешүүгө чакыруу жана 'Приглашен' статусуна өткөрүү."""
    if request.method == "POST":
        form = InterviewForm(request.POST)
        if form.is_valid():
            interview = form.save()

            # Колдонуучунун статусун 'Приглашен' кылуу
            interview.user.status = "invited"
            interview.user.save()

            formatted_date = interview.date_time.strftime("%Y-%m-%d %H:%M")

            # WhatsApp билдирүүсүн жөнөтүү
            return redirect('send_whatsapp_message',
                            whatsapp_number=interview.whatsapp_number,
                            mentor=interview.mentor,
                            date_time=formatted_date,
                            user_name=interview.user.name)
    else:
        form = InterviewForm()
    return render(request, 'users/schedule_interview.html', {'form': form})


def send_whatsapp_message(request, whatsapp_number, mentor, date_time, user_name):
    """WhatsApp аркылуу билдирүү жөнөтүү."""
    try:
        # Датаны туура форматка келтирүү
        parsed_date = datetime.strptime(date_time, "%Y-%m-%d %H:%M")
        formatted_date = parsed_date.strftime("%d-%m-%Y %H:%M")

        # WhatsApp үчүн билдирүү
        message = f"Саламатсызбы, {user_name}! Сиз {formatted_date} убакытка {mentor} менен маектешүүгө чакырылдыңыз."
        encoded_message = urllib.parse.quote(message)
        whatsapp_url = f"https://api.whatsapp.com/send?phone={whatsapp_number}&text={encoded_message}"
        return redirect(whatsapp_url)

    except Exception as e:
        return render(request, 'users/error.html', {'error': str(e)})





def toggle_theme(request):
    """Теманы алмаштыруу (light <-> dark)"""
    current_theme = request.COOKIES.get("theme", "light")
    new_theme = "dark" if current_theme == "light" else "light"

    response = redirect(request.META.get('HTTP_REFERER', 'settings'))
    response.set_cookie("theme", new_theme, max_age=60*60*24*365)  # 1 жыл сакталат

    return response



def settings_view(request):
    """Настройки барагы"""
    if request.method == "POST":
        response = redirect(reverse('settings'))  # <-- Бул туура!

        # Тема (Темный/Яркий)
        theme = request.POST.get("theme")
        if theme:
            response.set_cookie("theme", theme, max_age=60*60*24*365)  # 1 жыл сакталат

        # Тил тандоо (Русский, Кыргызча, English)
        language = request.POST.get("language")
        if language:
            response.set_cookie("language", language, max_age=60*60*24*365)

        # Дата форматын тандоо
        date_format = request.POST.get("date_format")
        if date_format:
            response.set_cookie("date_format", date_format, max_age=60*60*24*365)

        # WhatsApp чакыруу тексти
        whatsapp_text = request.POST.get("whatsapp_text")
        if whatsapp_text:
            request.session["whatsapp_text"] = whatsapp_text  # Session'го сактоо

        return response

    return render(request, "users/settings.html")