from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from book.models import Book, Review, Comment, Profile


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['subject', 'writer', 'publisher', 'content', 'photo']
        labels = {
            'subject': '제목',
            'writer': '저자',
            'publisher': '출판사',
            'content': '내용',
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['score', 'content']
        score = forms.IntegerField(
            required=True,
            label='평점',
            min_value=0,
            max_value=5,
            widget=forms.NumberInput(attrs={
                'class': 'score'
            })
        )
        labels = {
            'content': '리뷰내용',
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content': '댓글내용',
        }
