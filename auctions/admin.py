from django.contrib import admin

from .models import Lot, Bid, Comment, Category, User

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    filter_horizontal = ("watchlist", )

admin.site.register(Lot)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(User, UserAdmin)
