from .models import LinkPost
from django import forms
class LinkPostForm(forms.ModelForm):
    class Meta:
        model = LinkPost
        fields = '__all__' 