from django import forms
from .models import Post,Vote,Comment

class PostForm(forms.ModelForm):

    class Meta:
        model=Post
        fields=["Description","author","title","image"]

        widgets={
            'title': forms.TextInput(attrs={'class': 'textinputclass'}),
            "Description": forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'}),
            
        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)

        widgets = {
            'author': forms.TextInput(attrs={'class': 'textinputclass'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea'}),
        }