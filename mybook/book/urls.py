from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import base_views, book_views, review_views, comment_views, vote_views, profile_views, rent_views

app_name = 'book'


urlpatterns = [
    # base_views.py
    path('',
         base_views.index, name='index'),
    path('<int:book_id>/',
         base_views.detail, name='detail'),

    # book_views.py
    path('book/create/',
         book_views.book_create, name='book_create'),
    path('book/modify/<int:book_id>/',
         book_views.book_modify, name='book_modify'),
    path('book/delete/<int:book_id>/',
         book_views.book_delete, name='book_delete'),

    # review_views.py
    path('review/create/<int:book_id>/',
         review_views.review_create, name='review_create'),
    path('review/modify/<int:review_id>/',
         review_views.review_modify, name='review_modify'),
    path('review/delete/<int:review_id>/',
         review_views.review_delete, name='review_delete'),

    # comment_views.py
    path('comment/create/book/<int:book_id>/',
         comment_views.comment_create_book, name='comment_create_book'),
    path('comment/modify/book/<int:comment_id>/',
         comment_views.comment_modify_book, name='comment_modify_book'),
    path('comment/delete/book/<int:comment_id>/',
         comment_views.comment_delete_book, name='comment_delete_book'),

    path('comment/create/review/<int:review_id>/',
         comment_views.comment_create_review, name='comment_create_review'),
    path('comment/modify/review/<int:comment_id>/',
         comment_views.comment_modify_review, name='comment_modify_review'),
    path('comment/delete/review/<int:comment_id>/',
         comment_views.comment_delete_review, name='comment_delete_review'),

    # vote_views.py
    path('vote/book/<int:book_id>/',
         vote_views.vote_book, name='vote_book'),
    path('vote/review/<int:review_id>/',
         vote_views.vote_review, name='vote_review'),

    # profile_views.py
    # user.username 을 str 로 받는다.
    # user_id 는 int 로 받는다.
    path('user/<str:username>/',
         profile_views.people, name="people"),
    path('rentBook/<int:user_id>',
         profile_views.rent_books, name="rent_books"),
    path('rentBookAll/<int:user_id>',
         profile_views.rent_book_all, name="rent_book_all"),
    path('history/<int:user_id>',
         profile_views.rent_history, name="rent_history"),
    path('historyAll/<int:user_id>',
         profile_views.rent_history_all, name="rent_history_all"),

    # rent_views.py
    path('rent/<int:book_id>/',
         rent_views.rent_book, name='rent_book'),
    path('return/<int:book_id>/',
         rent_views.return_book, name='return_book'),
]

# 이미지 파일의 경로
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
