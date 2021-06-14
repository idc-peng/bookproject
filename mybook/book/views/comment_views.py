from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.utils import timezone


from ..forms import CommentForm
from ..models import Book, Review, Comment


@login_required(login_url='common:login')
def comment_create_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.create_date = timezone.now()
            comment.book = book
            comment.save()
            return redirect('{}#comment_{}'.format(resolve_url('book:detail',
                            book_id=comment.book.id), comment.id))
    else:
        form = CommentForm()
    context = {'form': form}
    return render(request, 'book/comment_form.html', context)


@login_required(login_url='common:login')
def comment_modify_book(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글수정권한이없습니다.')
        return redirect('book:detail', book_id=comment.book.id)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.modify_date = timezone.now()
            comment.save()
            return redirect('{}#comment_{}'.format(resolve_url('book:detail',
                            book_id=comment.book.id), comment.id))
    else:
        form = CommentForm(instance=comment)

    context = {'form': form}
    return render(request, 'book/comment_form.html', context)


@login_required(login_url='common:login')
def comment_delete_book(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글삭제권한이 없습니다')
        return redirect('book:detail', book_id=comment.book_id)
    else:
        comment.delete()

    return redirect('book:detail', book_id=comment.book_id)


@login_required(login_url='common:login')
def comment_create_review(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.create_date = timezone.now()
            comment.review = review
            comment.save()
            return redirect('{}#comment_{}'.format(resolve_url('book:detail',
                            book_id=comment.review.book.id), comment.id))
    else:
        form = CommentForm()
    context = {'form': form}
    return render(request, 'book/comment_form.html', context)


@login_required(login_url='common:login')
def comment_modify_review(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글수정권한이없습니다.')
        return redirect('book:detail', book_id=comment.review.book.id)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.modify_date = timezone.now()
            comment.save()
            return redirect('{}#comment_{}'.format(resolve_url('book:detail',
                            book_id=comment.review.book.id), comment.id))
    else:
        form = CommentForm(instance=comment)

    context = {'form': form}
    return render(request, 'book/comment_form.html', context)


@login_required(login_url='common:login')
def comment_delete_review(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글삭제권한이 없습니다')
        return redirect('book:detail', book_id=comment.review.book.id)
    else:
        comment.delete()

    return redirect('book:detail', book_id=comment.review.book.id)

