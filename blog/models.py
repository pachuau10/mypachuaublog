from django.db import models
from ckeditor.fields import RichTextField
# Create your models here.
from django.db import models
from django.utils import timezone
from cloudinary.models import CloudinaryField
from ckeditor_uploader.fields import RichTextUploadingField




class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    
    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.name
    


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    content = RichTextUploadingField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')
    image = CloudinaryField('image', blank=True, null=True)  # Cloudinary will handle
    author_image = CloudinaryField('author_image', blank=True, null=True)
    author = models.CharField(max_length=100, default="Pachuau")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)

    enable_code_runner = models.BooleanField(
        default=False, 
        help_text="Enable interactive code execution for code blocks in this post"
    )
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title

class Newsletter(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.email

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)  # Track if you've read it
    
    def __str__(self):
        return f"{self.name} - {self.email}"
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'