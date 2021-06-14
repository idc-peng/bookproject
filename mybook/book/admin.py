from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from django.contrib.auth.models import User
from .models import Book, RentHistory


class BookAdmin(admin.ModelAdmin):
    search_fields = ['subject']


@admin.register(RentHistory)
class RentHistoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'book', 'rent_start', 'rent_end', 'return_status']
    list_display_links = ['user', 'book']
# class ProfileInline(admin.StackedInline):
#     model = Profile
#     con_delete = False
#
#     class CustomUserAdmin(UserAdmin):
#         inlines = (ProfileInline,)


admin.site.register(Book, BookAdmin)
# admin.site.unregister(User)
# admin.site.register(User, CustomUserAdmin)
