from django import forms
from .models import Comment, Tweet, User


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ['tweet', 'date_added']


class AddTweet(forms.ModelForm):
    class Meta:
        model = Tweet
        exclude = ['date_added']


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'second_name', 'motto', 'image', 'gender')
