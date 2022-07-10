from datetime import date, timedelta

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Book(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='author_book')
    subject = models.CharField(max_length=200)
    writer = models.CharField(max_length=100)       # 저자
    publisher = models.CharField(max_length=100)    # 출판사
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_book')
    # 사진필드이다.
    photo = models.ImageField(blank=True, null=True)

    # 대출 정보
    rent_info = models.OneToOneField('RentHistory', on_delete=models.CASCADE,
                                     verbose_name='대출정보', blank=True, null=True, related_name='rent_book')

    def __str__(self):
        return self.subject

    def rent_book(self, user):  # 도서 대여
        rent_start = date.today()
        rent_end = date.today() + timedelta(days=7)
        rent_info = self.renthistory_set.create(user=user, rent_start=rent_start, rent_end=rent_end,
                                                return_status=False)
        self.rent_info = rent_info
        self.save()

    def return_book(self):      # 반납 메소드
        self.rent_info.return_status = True
        self.rent_info.return_date = date.today()
        self.rent_info.save()
        self.rent_info = None
        self.save()

    def get_rent_history(self):     # 대여 책 기록
        return RentHistory.objects.filter(user=self)


class Review(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='author_review')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_review')
    score = models.IntegerField(default=0)      # 평점


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    book = models.ForeignKey(Book, null=True, blank=True, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, null=True, blank=True, on_delete=models.CASCADE)


class Profile(models.Model):    # 프로필 만들기 common앱에 넣고 싶었으나 2가지 앱을 같이 사용하는게 미숙하였다.
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # user모델과 profile을 1대1로 연결하는 과정 | OneToOneField 일대일관계 | AUTH_USER_MODEL 현 계정의 사용자 갖고오기
    description = models.TextField(blank=True)
    nickname = models.CharField(max_length=20, blank=True)


class RentHistory(models.Model):    # 도서 대출 이력
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='대출회원')
    book = models.ForeignKey(Book, null=True, blank=True, on_delete=models.CASCADE)
    rent_start = models.DateField("대여시작일")
    rent_end = models.DateField("대여종료일")
    return_status = models.BooleanField("반납여부")
    return_date = models.DateField("반납일", blank=True, null=True)

    def __str__(self):
        return "{}-{}".format(self.user, self.book)
