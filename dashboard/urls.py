from nturl2path import url2pathname
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name ='home'),
    path('notes/', views.notes, name ='notes'),
    path('delete_note/<int:id>', views.delete_note, name ='delete_note'),
    
    path('notes_detail/(?P<pk>\d+)$', views.NotesDetailviews.as_view(), name ='notes_detail'),
   

    path('homework',views.homework,name = 'homework'),
    path('update_homework/<int:pk>',views.update_homework,name = 'update_homework'),
    path('delete_homework/<int:id>', views.delete_homework, name ='delete_homework'),

    path('book',views.books,name = 'book'),

    path('todo',views.todo,name = 'todo'),
    path('delete_todo/<int:pk>', views.delete_todo, name ='delete_todo'),
    path('update_todo/<int:pk>', views.update_todo, name ='update_todo'),
   


    
]
