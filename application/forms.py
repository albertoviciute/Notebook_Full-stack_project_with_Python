from django.contrib.auth.forms import UserCreationForm
from .models import User, Category, Note
from django import forms


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'image', 'password1', 'password2']


class CreateCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        widgets = {'user': forms.HiddenInput()}


class CreateNoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = '__all__'
        widgets = {'user': forms.HiddenInput()}
