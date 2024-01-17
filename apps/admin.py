from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

from .models import Approval,Requisition,Report,Workorder,Issue,ProductList,Purchase,StoreBalance,DepartmentList
from django.contrib import admin
from .models import ProductList
from django.db.models import Q

class CustomUserAdmin(UserAdmin):
    #add_form = CustomUserCreationForm
    model = CustomUser
    list_display = ('username', 'email', 'user_type')
    def get_plain_text_password(self, obj):
        return obj.plain_text_password

    get_plain_text_password.short_description = 'Plain Text Password'
    get_plain_text_password.admin_order_field = 'plain_text_password'

    list_display = UserAdmin.list_display + ('get_plain_text_password',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'user_type','photo')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'user_type'),
        }),
    )
class ProductAdmin(admin.ModelAdmin):
    search_fields = ['material_name']

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        # Add additional filtering logic if needed
        queryset = queryset.filter(material_name__icontains=search_term)

        return queryset, use_distinct

class DepartmentListAdmin(admin.ModelAdmin):
    search_fields = ['department_name']  # Add the field you want to search

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)

        # Add additional filtering logic if needed
        queryset = queryset.filter(department_name__icontains=search_term)

        return queryset, use_distinct

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(ProductList,ProductAdmin)
admin.site.register(DepartmentList,DepartmentListAdmin)
#admin.site.register(StoreBalance)
# admin.site.register(Approval)
#admin.site.register(Requisition)
# admin.site.register(Report)
# admin.site.register(Workorder)
#admin.site.register(Issue)
# admin.site.register(Purchase)
