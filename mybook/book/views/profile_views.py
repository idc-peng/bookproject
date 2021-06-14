from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from ..forms import Profile


from ..models import Book, Profile, RentHistory
# 유저의 프로필과 관련된 views 입니다.


@login_required(login_url='common:login')   # 프로필
def people(request, username):  # urls.py에서 넘겨준 인자를 username으로 받는다.
    person = get_object_or_404(get_user_model(), username=username)
    return render(request, 'common/people.html', {'person': person})

# .check_password(raw_password) : 암호를 비교한다.


@login_required
def rent_books(request, user_id):           # 대여 책
    books = get_object_or_404(RentHistory, pk=user_id)
    # filter(user_id=user_id, return_status=False)로 주어 해당 유저의 아이디면서 반납을 하지 않은 책이라는 뜻입니다.
    rent_book_list = RentHistory.objects.filter(user_id=user_id, return_status=False)
    context = {'books': books, 'rent_book_list': rent_book_list}
    return render(request, 'common/rent_books.html', context)


@login_required
def rent_book_all(request, user_id):        # 슈퍼 계정이 확인할 수 있는 모든 사용자의 현재 대여책
    so = request.GET.get('so', 'userID')

    # 장고 수업에서 배운 방법으로 작성하였습니다.
    if so == 'rent_date':   # 대여일순
        rent_book_list = RentHistory.objects.filter(return_status=False).order_by()
    else:                   # 유저순
        rent_book_list = RentHistory.objects.filter(return_status=False).order_by('user_id')

    books = get_object_or_404(RentHistory, pk=user_id)
    context = {'books': books, 'rent_book_list': rent_book_list, 'so': so}
    return render(request, 'common/rent_book_all.html', context)


@login_required
def rent_history(request, user_id):         # 대여 기록 확인
    books = get_object_or_404(RentHistory, pk=user_id)
    # 대여 기록이므로 (return_status)는 'True' 나 'False' 에 상관없이 출력하였습니다.
    rent_book_all_list = RentHistory.objects.filter(user_id=user_id)
    context = {'books': books, 'rent_book_all_list': rent_book_all_list}
    return render(request, 'common/rent_history.html', context)


@login_required
def rent_history_all(request, user_id):     # 모든 사용자의 대여 기록 확인
    so = request.GET.get('so', 'userID')

    # 정렬
    if so == 'rent_date':       # 대여일순
        rent_book_all_list = RentHistory.objects.filter().order_by()
    else:                       # 유저순
        rent_book_all_list = RentHistory.objects.filter().order_by('user_id')

    books = get_object_or_404(RentHistory, pk=user_id)
    context = {'books': books, 'rent_book_all_list': rent_book_all_list, 'so': so}
    return render(request, 'common/rent_history_all.html', context)
