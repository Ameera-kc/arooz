from django.contrib import admin
from user.models import (
    AddToCart,
    AdminNumber,
    AvailableSizes,
    Cart,
    Category,
    ChangePassword,
    Event,
    HeaderFlash,
    Login,
    MainBanner,
    Measurements,
    Product,
    Size,
    SubBanners1,
    SubBanners2,
    SubCategory,
    Wishlist,
)
from django.contrib import messages
from django.utils.translation import ngettext


# def mark_active(self, request, queryset):
#     updated = queryset.update(is_active=True)
#     self.message_user(request, ngettext("%d object was successfully marked as active.", "%d objects were successfully marked as active.", updated) % updated, messages.SUCCESS)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["category"]


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(MainBanner)
class MainBannerAdmin(admin.ModelAdmin):
    pass


@admin.register(SubBanners1)
class SubBanners1Admin(admin.ModelAdmin):
    pass


@admin.register(SubBanners2)
class SubBanners2Admin(admin.ModelAdmin):
    pass


@admin.register(HeaderFlash)
class HeaderFlashAdmin(admin.ModelAdmin):
    pass


@admin.register(Login)
class LoginAdmin(admin.ModelAdmin):
    pass


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    pass


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    pass


@admin.register(AddToCart)
class AddToCartAdmin(admin.ModelAdmin):
    pass


@admin.register(ChangePassword)
class ChangePasswordAdmin(admin.ModelAdmin):
    pass


@admin.register(AdminNumber)
class AdminNumberAdmin(admin.ModelAdmin):
    pass


@admin.register(Measurements)
class MeasurementsAdmin(admin.ModelAdmin):
    pass


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    pass


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass


@admin.register(AvailableSizes)
class AvailableSizesAdmin(admin.ModelAdmin):
    pass
