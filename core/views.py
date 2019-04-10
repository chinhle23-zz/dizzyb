from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import Http404
from django.contrib import messages

from .forms import NewTaskForm, NoteForm
from datetime import date

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return redirect('task_list')

    return render(request, "core/index_logged_out.html")


@require_http_methods(['GET', 'POST'])
@login_required
def edit_task(request, task_id):
    task = request.user.tasks.with_hashid(task_id)
        # 'tasks' is the related name of the owner field in the Task model
        # hashid?
    if task is None:
        raise Http404('No task matches the given query.')

    if request.method == 'POST':
        # if user is submitting a form
        form = EditTaskForm(instance=task, data=request.POST)
        if form.save():
            return redirect('task-list')
    else:
        # else make a new form
        form = EditTaskForm(instance=task)

    note_form = NoteForm()

    return render(request, 'core/edit_task.html', {'form':form, 'note_form': note_form, 'task': task})

@require_http_methods(['POST'])
@login_required
def new_note(request, task_id):
    task = request.user.tasks.with_hashid(task_id)
    if task is None:
        raise Http404('No task matches the given query.') 

    form = NoteForm(request.POST)

    if form.is_valid():
        note = form.save(commit=False)
            # don't actually save to the database yet
        note.task = task
        note.save()
    else:
        messages.error(request, 'We have a problem saving your note.')

    return redirect(to='edit_task', task_id=task.pk)
    # return redirect(to='edit_task', task_id=task.hashid)

@require_http_methods(['POST'])
@login_required
def new_task(request, task_id):
    form = NewTaskForm(request.POST)
    if form.is_valid():
        form.save(owner=request.user)
    return redirect('task_list')