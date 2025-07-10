from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from .forms import TaskForm
from .models import Task

def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'tasks/task_list.html', {'tasks': tasks})


def task_add(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save()
            messages.success(request, 'Задача добавлена')
            return redirect('task_detail', pk=task.pk)
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form})


def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'tasks/task_detail.html', {'task': task})


def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Задача обновлена')
            return redirect('task_detail', pk=task.pk)
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form})


def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Задача удалена')
        return redirect('task_list')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})


def task_bulk_delete(request):
    if request.method == 'POST':
        ids = request.POST.getlist('task_ids')
        deleted_count, _ = Task.objects.filter(id__in=ids).delete()
        messages.success(request, f"Удалено задач: {deleted_count}")
    return redirect('task_list')
