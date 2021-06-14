from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render


from ..models import Book
# 책 대여에 관한 views 입니다.


@login_required
def rent_book(request, book_id):        # 책 대여
    book = get_object_or_404(Book, pk=book_id)
    book.rent_book(request.user)
    messages.info(request, '대여하였습니다! 반납 예정일은 {} 입니다.'.format(book.rent_info.rent_end))
    return redirect('book:detail', book_id=book.id)


@login_required
def return_book(request, book_id):           # 책 반납
    book = get_object_or_404(Book, pk=book_id)
    if book.rent_info.user == request.user:
        book.return_book()
        messages.info(request, '반납하였습니다!')
    else:           # 빌린 유저와 반납 유저가 다를 경우 반납 실패를 출력하였습니다.
        messages.error(request, '반납을 실패하였습니다!')
    return redirect('book:detail', book_id=book_id)
