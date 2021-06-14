from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Count, Avg

from ..models import Book, Review


def index(request):
    page = request.GET.get('page', '1')
    kw = request.GET.get('kw', '')
    so = request.GET.get('so', 'recent')

    # 정렬
    if so == 'recommend':
        book_list = Book.objects.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        book_list = Book.objects.annotate(num_review=Count('review')).order_by('-num_review', '-create_date')
    else:  # recent
        book_list = Book.objects.order_by('-create_date')

    # 키워드
    if kw:
        book_list = book_list.filter(
            Q(subject__icontains=kw) |                 # 제목검색
            Q(content__icontains=kw) |                 # 내용검색
            Q(author__username__icontains=kw) |        # 질문 글쓴이검색
            Q(review__author__username__icontains=kw)  # 답변 글쓴이검색
        ).distinct()

    paginator = Paginator(book_list, 10)
    page_obj = paginator.get_page(page)
    context = {'book_list': page_obj, 'page': page, 'kw': kw, 'so': so}
    return render(request, 'book/book_list.html', context)


def detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    score_list = Review.objects.filter(book_id=book_id).aggregate(Avg('score'))
    score_avg = score_list.get('score__avg')
    context = {'book': book, 'score_avg': score_avg}
    return render(request, 'book/book_detail.html', context)
