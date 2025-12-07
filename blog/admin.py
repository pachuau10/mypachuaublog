from django.contrib import admin
from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import Category, BlogPost, Newsletter, ContactMessage

# Form to use CKEditor in admin
class BlogPostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())  # Rich editor
    class Meta:
        model = BlogPost
        fields = '__all__'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    form = BlogPostAdminForm  # <-- use CKEditor form
    list_display = ['title', 'category', 'author', 'enable_code_runner', 'created_at', 'is_published']
    list_filter = ['category', 'is_published', 'enable_code_runner', 'created_at']
    search_fields = ['title', 'description', 'content']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    list_editable = ['enable_code_runner']  # Quick toggle from list view
    
    fieldsets = (
        ('Post Info', {
            'fields': ('title', 'slug', 'category', 'is_published')
        }),
        ('Content', {
            'fields': ('description', 'content', 'image')
        }),
        ('Interactive Features', {
            'fields': ('enable_code_runner',),
            'classes': ('collapse',),
            'description': 'Enable code execution for code blocks in this post'
        }),
        ('Author Info', {
            'fields': ('author', 'author_image')
        }),
    )

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['email', 'subscribed_at']
    search_fields = ['email']

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'created_at', 'is_read']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'message']
    readonly_fields = ['created_at']
    list_editable = ['is_read']  # Mark as read directly from list (CORRECT - this is for ContactMessage)
    
    fieldsets = (
        ('Contact Info', {
            'fields': ('name', 'email', 'is_read')
        }),
        ('Message', {
            'fields': ('message',)
        }),
        ('Timestamp', {
            'fields': ('created_at',)
        }),
    )