from django.contrib import admin
from game.models import HouseList,Guard,Coupon,UserInfo,Window,Officer


class HouseListAdmin(admin.ModelAdmin):
    list_display = ('address')

class GuardAdmin(admin.ModelAdmin):
    list_display = ('name')

class CouponAdmin(admin.ModelAdmin):
    list_display = ('name')

admin.site.register(HouseList)
admin.site.register(Guard)
admin.site.register(Coupon)
admin.site.register(UserInfo)
admin.site.register(Window)
admin.site.register(Officer)