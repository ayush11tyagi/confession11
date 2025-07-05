from django import forms
from .models import Confession

class ConfessionForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'confession-textarea',
            'placeholder': 'Share your anonymous confession here...',
            'rows': 6,
            'maxlength': 1000
        }),
        max_length=1000,
        help_text='Maximum 1000 characters'
    )
    
    class Meta:
        model = Confession
        fields = ['content'] 