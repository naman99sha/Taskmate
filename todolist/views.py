from django.shortcuts import render,redirect
from django.http import HttpResponse
from todolist.models import TaskList
from todolist.form import TaskForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required()
def todolist(request):
    if request.method=='POST':
        form=TaskForm(request.POST or None)
        if form.is_valid():
            form.save(commit=False).manager=request.user
            form.save()
        messages.success(request,("New Task Added!!"))
        return redirect('todolist')

    else:
        all_tasks=TaskList.objects.filter(manager=request.user)
        paginator=Paginator(all_tasks,5)
        page=request.GET.get('pg')
        all_tasks=paginator.get_page(page)
        return render(request,'todolist.html',{'all_tasks':all_tasks})


def contact(request):
    context={'contact_text':'Welcome to Contact page'}
    return render(request,'contact.html',context)

def about(request):
    context={'about_text':'Welcome to About page'}
    return render(request,'about.html',context)

def index(request):
    context={'index_text':'Welcome to Home page'}
    return render(request,'index.html',context)

@login_required()
def delete_task(request,task_id):
    task=TaskList.objects.get(pk=task_id)
    if task.manager == request.user:
        task.delete()
    else:
        messages.error(request,("Unauthorized Access!!"))

    return redirect('todolist')

@login_required()
def edit_task(request,task_id):
    if request.method=='POST':
        task_object=TaskList.objects.get(pk=task_id)
        form=TaskForm(request.POST or None,instance=task_object)
        if form.is_valid():
            form.save()
        messages.success(request,("Task Edited!!"))
        return redirect('todolist')

    else:
        task_object=TaskList.objects.get(pk=task_id)

        return render(request,'edit.html',{'task_obj':task_object})

@login_required()
def complete_task(request,task_id):
    task=TaskList.objects.get(pk=task_id)
    if task.manager == request.user:
        task.done=True
        task.save()
    else:
        messages.error(request,("Unauthorized Access!!"))
    return redirect('todolist')

@login_required()
def pending_task(request,task_id):
    task=TaskList.objects.get(pk=task_id)
    if task.manager == request.user:
        task.done=False
        task.save()
    else:
        messages.error(request,("Unauthorized Access!!"))
    return redirect('todolist')
