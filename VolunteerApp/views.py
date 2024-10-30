from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Task, VolunteerProfile, Reward
from .forms import TaskForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import RegisterForm
from django.shortcuts import render, get_object_or_404, redirect
from .models import Task

def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'task_list.html', {'tasks': tasks})

def invite_to_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == "POST":
        if task.current_participants.count() < task.max_participants:
            task.current_participants.add(request.user)
            task.save()
            # Optionally, you can display a success message here
        else:
            # Optionally, handle the case where the task is full
            pass
    return redirect('task_list')

def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.user.is_staff:  # Ensure only admin can complete the task
        task.is_completed = True
        task.save()
        # Add logic to credit hours to participants
        for user in task.current_participants.all():
            user.profile.hours += task.hours_reward  # Assuming User has a related Profile model
            user.profile.save()
    return redirect('task_list')

def home(request):
    if request.user.is_authenticated:
        return redirect('base')
    return redirect('login')

@login_required
def base(request):
    return render(request, 'base.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful.")
            return redirect('login')
        else:
            messages.error(request, "Registration failed. Please correct the errors below.")
    else:
        form = RegisterForm()
    return render(request, 'VolunteerApp/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('base')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'VolunteerApp/login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.info(request, "Logged out successfully.")
    return redirect('login')

@login_required

def profile(request):
    profile = get_object_or_404(VolunteerProfile, user=request.user)
    return render(request, 'VolunteerApp/profile.html', {'profile': profile})
@login_required
def create_task(request):
    if request.user.is_staff:
        form = TaskForm()
        if request.method == 'POST':
            form = TaskForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('task_list')
        return render(request, 'VolunteerApp/create_task.html', {'form': form})
    return redirect('task_list')



def leaderboard(request):
    volunteers = VolunteerProfile.objects.all().order_by('-total_hours')
    return render(request, 'VolunteerApp/leaderboard.html', {'volunteers': volunteers})

@login_required
def rewards(request):
    profile = VolunteerProfile.objects.get(user=request.user)
    rewards = Reward.objects.filter(required_hours__lte=profile.total_hours)
    return render(request, 'VolunteerApp/rewards.html', {'rewards': rewards})