from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .models import Task
from .forms import TaskForm


def home(request):
    return render(request, 'home.html')


@login_required
def create(request):
    if request.method == 'GET':
        return render(request, 'task/create.html', {'form': TaskForm()})
    else:
        try:
            form = TaskForm(request.POST)
            task = form.save(commit=False)
            task.author = request.user
            task.save()
            return redirect('current')
        except ValueError:
            return render(request, 'task/create.html', {'form': TaskForm(), 'error': 'Bad data passed in!'})


@login_required
def current(request):
    tasks = Task.objects.filter(author=request.user, completed__isnull=True).order_by('-created')
    return render(request, 'task/current.html', {'tasks': tasks})


@login_required
def completed(request):
    tasks = Task.objects.filter(author=request.user, completed__isnull=False).order_by('-completed')
    return render(request, 'task/completed.html', {'tasks': tasks})


@login_required
def detail(request, pk):
    task = get_object_or_404(Task, pk=pk, author=request.user, completed__isnull=True)
    if request.method == 'GET':
        form = TaskForm(instance=task)
        return render(request, 'task/detail.html', {'form': form, 'task': task})
    else:
        try:
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('current')
        except ValueError:
            return render(request, 'task/detail.html',
                          {'form': TaskForm(), 'task': task, 'error': 'Bad data passed in!'})


@login_required
def complete(request, pk):
    if request.method == "POST":
        task = get_object_or_404(Task, pk=pk, author=request.user)
        task.completed = timezone.now()
        task.save()
        return redirect('current')


@login_required
def delete(request, pk):
    if request.method == "POST":
        task = get_object_or_404(Task, pk=pk, author=request.user)
        task.delete()
        return redirect('current')
