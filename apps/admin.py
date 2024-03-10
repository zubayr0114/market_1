from django.contrib import admin
from django.contrib.admin import ModelAdmin, StackedInline
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.forms import ModelForm
from django.utils.safestring import mark_safe
from mptt.admin import DraggableMPTTAdmin

from apps.models import Category, Product, ProductImage, SiteSettings, User


class CategoryModelForm(ModelForm):
    class Meta:
        model = Category
        exclude = ()


@admin.register(Category)
class CategoryMPTTModelAdmin(DraggableMPTTAdmin):
    mptt_level_indent = 20
    form = CategoryModelForm


class ProductImageStackedInline(StackedInline):
    model = ProductImage
    min_num = 1
    extra = 0
    fields = ['image']


@admin.register(Product)
class ProductModelAdmin(ModelAdmin):
    inlines = (ProductImageStackedInline,)
    list_display = ["id", "name", "form_description", "price", "quantity", 'image_show', "category",
                    "created_at_product"]
    search_fields = ['id', 'name']

    def form_description(self, obj):
        return mark_safe(obj.description)

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super(ProductModelAdmin, self).get_queryset(request)

        #     return super(ProductAdmin, self).get_queryset(request)
        else:
            qs = super(ProductModelAdmin, self).get_queryset(request)
        return qs.filter(owner=request.user)

    def image_show(self, obj: Product):
        if obj.images.first():
            return mark_safe("<img src='{}' width='50' />".format(obj.images.first().image.url))

        return ''

    image_show.description = 'images'


@admin.register(User)
class BaseUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (('Personal info'),
         {'fields': ('first_name', 'last_name', 'email', 'avatar', 'workout', 'country', 'is_verified', 'banner')}),
        (('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'avatar',),
        }),
    )
    # inlines = (UserImageStackedInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ['delivery_price']

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.unregister(Group)
