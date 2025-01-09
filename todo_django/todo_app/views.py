from django.shortcuts import render, redirect
from django.db import connection
from .forms import TaskForm

def index(request):
    form = TaskForm()
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            # Saving using SQL
            title = form.cleaned_data['title']
            status = form.cleaned_data.get('status', False)
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO todo_app_task (title, status) VALUES (%s, %s)", [title, status])
            return redirect('home')

    # Fetching tasks using SQL
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, title, status FROM todo_app_task")
        tasks = [{'id': row[0], 'title': row[1], 'status': row[2]} for row in cursor.fetchall()]

    context = {'tasks': tasks, 'form': form}
    return render(request, 'todo_app/index.html', context)

def updateTask(request, task_id):
    with connection.cursor() as cursor:
        cursor.execute("UPDATE todo_app_task SET status = %s WHERE id = %s", [True, task_id])
    return redirect('home')

def deleteTask(request, task_id):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM todo_app_task WHERE id = %s", [task_id])
    return redirect('home')
