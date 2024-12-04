from django.contrib import admin
from blog.models import Category, Comment, Post, CustomUser
from django.contrib.auth.admin import UserAdmin

class CategoryAdmin(admin.ModelAdmin):
    pass

class PostAdmin(admin.ModelAdmin):
    pass

class CommentAdmin(admin.ModelAdmin):
    pass

# You can customize how the CustomUser is displayed in the admin by using the UserAdmin class
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # List of fields to display in the admin user list view
    list_display = ('username', 'email', 'first_name', 'last_name', 'birthdate', 'is_staff')
    # Fields displayed when editing a user in the admin interface
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'birthdate', 'phone_number', 'profile_picture')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    # Fields to display in the list view
    list_filter = ('is_staff', 'is_superuser', 'groups')

# Register the CustomUser model with the admin site
admin.site.register(CustomUser, CustomUserAdmin)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
