from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

class PostForms(forms.ModelForm):
    title = forms.CharField(
        max_length=60,
        widget=forms.TextInput(
            attrs={"class":"form-control", "placeholder":"Give a Cool Title!"}
        ),
    )
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.SelectMultiple(
            attrs={"class": "form-control"}
        ),
        required=True  # Change to False if categories are optional
    )
    body = forms.CharField(
        widget=forms.Textarea(
            attrs={"class": "form-control", "placeholder": "Tell us your Awesome Story!"}
        )
    )
    image = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'input'})
    )

    class Meta:
        model = Post
        fields = ['title', 'categories', 'body', 'image']




class CommentForms(forms.ModelForm):
    author = forms.CharField(
        max_length=60,
        widget=forms.TextInput(
            attrs={"class":"form-control", "placeholder":"Your Name"}
        ),
    )
    body = forms.CharField(
        widget=forms.Textarea(
            attrs={"class":"form-control", "placeholder":"Leave a cool comment!"}
        )
    )
    class Meta:
        model = Comment
        fields = ['author', 'body']
