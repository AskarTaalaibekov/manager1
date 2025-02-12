from django.shortcuts import render, get_object_or_404, redirect
from .models import UserProfile
from .forms import UserForm

def user_list(request):
    status_filter = request.GET.get('status')
    direction_filter = request.GET.get('direction')

    users = UserProfile.objects.all()

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
            updated_user = form.save(commit=False)
            updated_user.updated_by = request.user
            updated_user.save()
            return redirect('user_list')
    else:
        form = UserForm(instance=user)
    return render(request, 'users/edit_user.html', {'form': form, 'user': user})


def change_status(request, user_id, status):
    user = get_object_or_404(UserProfile, id=user_id)
    user.status = status
    user.updated_by = request.user
    user.save()
    return redirect('user_list')