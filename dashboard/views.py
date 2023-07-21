
from multiprocessing import context
from socket import gaierror
from turtle import RawTurtle
from django.contrib import messages
from django.shortcuts import render , redirect
from . models import *
from .  forms import *

from django.views import generic
#from youtubesearchpython import VideosSearch
# Create your views here.
import requests


def home(request):
    return render(request,'dashboard\home.html')
    
def notes(request):

    if request.method == "POST":       
        form = NotesForm(request.POST)  
        if form.is_valid:
            notes = Notes(
            user=request.user,
            title=request.POST['title'],
            description=request.POST["description"],
            )
            notes.save()
            messages.success(request,f'Notes Added form {request.user } Successfully!!')
    
    notesForms=NotesForm()
    notes =  Notes.objects.filter(user=request.user)
    context = {
        'notes':notes,
        'notesForms':notesForms
    }

    return render(request,'dashboard/notes.html',context)

def delete_note(request,id= None):
    Notes.objects.get(id=id).delete()
    return redirect("notes")

class NotesDetailviews(generic.DetailView):
    model = Notes

def homework(request):
    if request.method == "POST":
        homeworkform = HomeworkForm(request.POST)
        if homeworkform.is_valid:
            try:
                finished = request.POST["is_finished"]
                if finished == 'on':
                    finished  = True
                else:
                    finished  = False
            except:
                finished = False
            homework = Homework(
            user=request.user,
            subject = request.POST['subject'],
            title=request.POST['title'],
            description=request.POST["description"],
            due = request.POST['due'],
            is_finished = finished,
            )
            homework.save()
            messages.success(request,f'Homework Added form {request.user} Successfully!!')
            


    else:
        homeworkform = HomeworkForm()
    works = Homework.objects.filter(user=request.user)
    if len(works) == 0:
        homework_done = True
    else:
        homework_done = False

    context = {
        'works':works,
        'homeworkform':homeworkform,
        'done':homework_done,
    }
    return render(request,'dashboard/homework.html',context)

def delete_homework(request,id =None):
    delete_is = Homework.objects.get(id=id).delete()
    return redirect("homework")

def update_homework(request,pk = None):
    homework = Homework.objects.get(id = pk)
    
    if homework.is_finished == True:
        homework.is_finished = False
    else:
        homework.is_finished = True
    homework.save()
    return redirect('homework')


def books(request):
    
    if request.method == "POST":
        try:
            form = DashboardForm(request.POST)
            text = request.POST['text']
            url = "https://www.googleapis.com/books/v1/volumes?q="+text
            
            r = requests.get(url)
            answer = r.json()

            result_list = []
            for i in range(10):
                result_dict = {
                    'title':answer['items'][i]['volumeInfo']['title'],
                    'subtitle':answer['items'][i]['volumeInfo'].get('subtitle'),
                    'description':answer['items'][i]['volumeInfo'].get('description'),
                    'count':answer['items'][i]['volumeInfo'].get('pageCount'),
                    'categories':answer['items'][i]['volumeInfo'].get('categories'),
                    'rating':answer['items'][i]['volumeInfo'].get('pageRating'),
                    'thumbnail':answer['items'][i]['volumeInfo'].get('imageLinks').get('thumbnail'),
                    'preview':answer['items'][i]['volumeInfo'].get('previewLink'),
                    }
            
                result_list.append(result_dict)
               
                context = {
                'search':form,
                'results':result_list,
                } 
            return render(request,'dashboard/books.html',context ) 
        except:
            messages.success(request,f"obs ----> book not found ( {text} ) !! ")
    else:
        form = DashboardForm()
    context = {
        'search':form
    }

    return render(request,"dashboard/books.html",context)

def todo(request):
    if request.method == 'POST':
       form = TodoForm(request.POST) 
       if form.is_valid:
            try:
                finished = request.POST["is_finished"]
                if finished == 'on':
                    finished = True
                else:
                    finished = False
            except:
                finished = False
            todos = Todo(
                user = request.user,
                title = request.POST['title'],
                is_finished = finished,
            )
            todos.save()
            messages.success(request,f"Todo Added form {request.user} !! ")
            
    else:
        form = TodoForm()
    todo = Todo.objects.filter(user=request.user)
    if len(todo) == 0:
        is_done = True
    else:
        is_done = False
    context = {
        'form':form,
        'todos': todo,
        'done':is_done,
    }
    
    return render(request,'dashboard/todo.html',context)

def update_todo(request,pk= None):
    todo =Todo.objects.get(id = pk)
    
    if todo.is_finished == True:
        todo.is_finished = False
    else:
        todo.is_finished = True
    todo.save()
    return redirect('todo')

def delete_todo(request,pk= None):
    delete = Todo.objects.get(id=pk).delete()
    return redirect('todo')

def register(request):
    if request.method == 'POST':
        form  = UserRegiesterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f'Account Creaated for {username}')
            return redirect("login")
    else:
        form = UserRegiesterForm()
    context = {
        'form':form
    }
    return render(request,"dashboard/register.html",context)


def profile(request):
    homeworks = Homework.objects.filter(is_finished=False,user= request.user)
    todos = Todo.objects.filter(is_finished=False,user= request.user)

    if len(homeworks) == 0:
        homework_done = True
    else:
        homework_done = False

    if len(todos) == 0:
        todo_done = True
    else:
        todo_done = False

    context = {
       'homeworks' :homeworks,
       'todos' : todos,
       'homework_done': homework_done,
       'todo_done':todo_done,  
    }

    return render(request,"dashboard/profile.html",context)