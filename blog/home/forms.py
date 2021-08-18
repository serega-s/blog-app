from django import forms
from froala_editor.widgets import FroalaEditor
from mptt.forms import TreeNodeChoiceField

from .models import *


class BlogForm(forms.ModelForm):
    class Meta:
        model = BlogModel
        fields = ['content', 'featured', 'is_draft']


class NewCommentForm(forms.ModelForm):
    parent = TreeNodeChoiceField(queryset=Comment.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['parent'].label = ''
        self.fields['parent'].required = False

    class Meta:
        model = Comment
        fields = ['post', 'parent', 'content']
