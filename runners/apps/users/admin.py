# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

# Form
from runners.apps.users.forms import UserAdminChangeForm, UserAdminCreationForm

# Admin
from runners.apps.users.models import User
from runners.bases.admin import Admin


# Main Section
@admin.register(User)
class UserAdmin(Admin, UserAdmin):
    list_display = ('profile_image_tag', 'email', 'phone', 'name', 'username', 'is_deleted')
    search_fields = ('email', 'username', 'name', 'phone')
    ordering = ('-created',)

    # Form
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    fieldsets = (
        ('1. 정보', {'fields': ('id', 'email', 'phone', 'name', 'username', 'password')}),
        ('2. 이미지', {'fields': ('profile_image_tag', 'profile_image', 'profile_image_url')}),
        ('3. 권한', {'fields': ('is_staff', 'is_superuser')}),
        ('4. 토큰', {'fields': ('auth_token',)}),
        ('5. 활성화 / 삭제 여부', {'fields': ('is_active', 'is_deleted', 'deleted')}),
        ('6. 생성일 / 수정일', {'fields': ('created', 'modified')}),
    )

    add_fieldsets = (
        ('1. 정보', {'fields': ('email', 'password1', 'password2')}),
        ('2. 권한', {'fields': ('is_staff', 'is_superuser')}),
    )

    readonly_fields = ('created', 'modified', 'deleted', 'auth_token', 'profile_image_tag', 'profile_image_url')

    def profile_image_tag(self, obj):
        profile_image_url = None

        if obj.profile_image_url:
            profile_image_url = obj.profile_image_url

        if obj.profile_image:
            profile_image_url = obj.profile_image.url

        if profile_image_url:
            return format_html(
                '<img src="{}" width="60px;" style="border: 1px solid lightgray; border-radius: 100%;"/>'.format(
                    profile_image_url)
            )
        else:
            return '-'

    profile_image_tag.short_description = '프로필 미리보기'
