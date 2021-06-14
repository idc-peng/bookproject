from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone


from ..forms import BookForm
from ..models import Book


@login_required(login_url='common:login')
def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.author = request.user
            book.create_date = timezone.now()
            book.save()
            return redirect('book:index')
    else:
        form = BookForm()
    context = {'form': form}
    return render(request, 'book/book_form.html', context)


@login_required(login_url='common:login')
def book_modify(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.user != book.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('book:detail', book_id=book.id)

    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            book = form.save(commit=False)
            book.author = request.user
            book.modify_date = timezone.now()
            book.save()
            return redirect('book:detail', book_id=book.id)
    else:
        form = BookForm(instance=book)
    context = {'form': form}
    return render(request, 'book/book_form.html', context)


@login_required(login_url='common:login')
def book_delete(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.user != book.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('book:detail', book_id=book.id)
    book.delete()
    return redirect('book:index')
