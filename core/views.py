from django.shortcuts import render, redirect, resolve_url
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import Http404
from django.contrib import messages
from .models import Tag
from .forms import NewTaskForm, NoteForm
from datetime import date

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return redirect('task_list')

    return render(request, "core/index_logged_out.html")

@login_required
def task_list(request, group=None, tag=None):
    tasks = request.user.tasks
    tags = Tag.objects.filter(tasks__owner=request.user).distinct()

    header_text = 'Current tasks'

    if group == 'complete':
        tasks = tasks.complete()
        header_text = 'Completed tasks'
    elif group == 'future':
        tasks = tasks.future()
        header_text = 'Future tasks'
    else:
        tasks = tasks.current()
    
    if tag is not None:
        tasks = tasks.filter(tags__text__iexact=tag)
            # https://docs.djangoproject.com/en/2.2/topics/db/queries/#retrieving-specific-objects-with-filters
            # https://docs.djangoproject.com/en/2.2/ref/models/querysets/#std:fieldlookup-iexact
        header_text += f' tagged #{tag}'
    
    context = {
        'today': date.today,
        'tasks': tasks,
        'tags': tags,
        'form': NewTaskForm()
    }

    return render(request, 'core/task_list.html', context=context)

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
        if form.is_valid():
            form.save()
            return redirect('task-list')
    else:
        # else make a new form
        form = EditTaskForm(instance=task)

    ### statements below run when none of the if statements above hit due to errors/invalid input ###

    note_form = NoteForm()

    return render(request, 'core/edit_task.html', {
        'form':form, 
        'note_form': note_form, 
        'task': task, 
        'notes': task.notes.order_by('created_at')
        })

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

    redirect_url = resolve_url(to='edit_task', task_id=task.pk)
    # redirect_url = resolve_url(to='edit_task', task_id=task.hashid)

    return redirect(to=f'{redirect_url}#note-{note.pk}')
        # '#' hashtag used in URL to be able to redirect with anchor, so page does not refresh to top of page each time a new note is added.

@require_http_methods(['POST'])
@login_required
def new_task(request, task_id):
    form = NewTaskForm(request.POST)
    if form.is_valid():
        form.save(owner=request.user)
    return redirect('task_list')