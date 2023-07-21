from dataclasses import fields
from tkinter import Widget
from django import forms
from . models import *
from django.contrib.auth.forms import UserCreationForm # for login


class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ["title","description"]

class Dateinput(forms.DateInput):
    input_type = 'date'

class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        widgets = {'due':Dateinput()}
        fields = [
            'subject',
            'title',
            'description',
            'due',
            'is_finished',
        ]
        
class DashboardForm(forms.Form):
    text = forms.CharField(
        max_length=200,
        label="Enter your Search",
        widget=forms.TextInput(attrs={
            'class': 'form-control',  # Add a CSS class for styling (Bootstrap class used here)
            'placeholder': 'Type your search query here...',  # Placeholder text in the input field
            'autocomplete': 'off',  # Disable autocomplete for this field
            'autocapitalize': 'none',  # Disable automatic capitalization
        }),
    )


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title','is_finished']


class UserRegiesterForm(UserCreationForm):
    class Meta:
        model = User 
        fields = ['username','password1','password2']
