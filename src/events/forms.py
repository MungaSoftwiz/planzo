from django import forms
from .models import Event # import models in the current module

class EventCreationForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'poster', 'venue', 'date', 'size', 'price']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'date'       :forms.TextInput(attrs={'type':'datetime-local'}),
        }

class EventEditForm(forms.ModelForm): # EventEditForm required
    class Meta:
        model = Event
        fields = ['title', 'description', 'poster', 'venue', 'date', 'size', 'price']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control'}), # Bootstrap CSS class form-control to style it
            'date'       :forms.TextInput(attrs={'type':'datetime-local'}),
        } 
        
