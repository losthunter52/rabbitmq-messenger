from django import forms
from .models import *

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = "__all__"

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = "__all__"
