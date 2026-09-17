from django import forms
from .models import Topic,Entry
 
class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic  # tels django This form is connected to the Topic model.
        fields = ['text']
        labels = {'text': ''}
        
class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text': ''}
        widgets = {'text': forms.Textarea(attrs={'cols': 80})} #  text area will be 80 columns wide instead of the default 40. This will give users enough room to write a meaningful entry