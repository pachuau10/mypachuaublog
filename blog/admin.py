from django.contrib import admin
from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import Category, BlogPost, Newsletter

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
    list_display = ['title', 'category', 'author', 'created_at', 'is_published']
    list_filter = ['category', 'is_published', 'created_at']
    search_fields = ['title', 'description', 'content']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['email', 'subscribed_at']
    search_fields = ['email']
