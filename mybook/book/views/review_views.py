from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone


from ..forms import ReviewForm
from ..models import Book, Review


@login_required(login_url='common:login')
def review_create(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.author = request.user
            review.book = book
            review.create_date = timezone.now()
            review.save()
            return redirect('{}#review_{}'.format(
                resolve_url('book:detail', book_id=book.id), review.id))
    else:
        form = ReviewForm()

    context = {'form': form, 'book': book}
    return render(request, 'book/book_detail.html', context)


@login_required(login_url='common:login')
def review_modify(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    if request.user != review.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('book:detail', book_id=review.book.id)

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            review = form.save(commit=False)
            review.author = request.user
            review.modify_date = timezone.now()
            review.save()
            return redirect('{}#review_{}'.format(
                resolve_url('book:detail', book_id=review.book.id), review.id))
    else:
        form = ReviewForm(instance=review)
    context = {'review': review, 'form': form}
    return render(request, 'book/review_form.html', context)


@login_required(login_url='common:login')
def review_delete(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    if request.user != review.author:
        messages.error(request, '삭제권한이 없습니다')
    else:
        review.delete()
    return redirect('book:detail', book_id=review.book.id)
