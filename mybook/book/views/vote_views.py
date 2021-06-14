from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect


from ..models import Book, Review


@login_required(login_url='common:login')
def vote_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.user == book.author:
        messages.error(request, '본인이 작성할 글은 추천할 수 없습니다')
    else:
        book.voter.add(request.user)
    return redirect('book:detail', book_id=book.id)


@login_required(login_url='common:login')
def vote_review(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    if request.user == review.author:
        messages.error(request, '본인이 작성할 글은 추천할 수 없습니다')
    else:
        review.voter.add(request.user)
    return redirect('book:detail', book_id=review.book.id)
