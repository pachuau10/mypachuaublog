from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from .models import BlogPost, Category, Newsletter

from django.core.paginator import Paginator

def home(request):
    posts = BlogPost.objects.filter(is_published=True)

    category_slug = request.GET.get('category')
    if category_slug:
        posts = posts.filter(category__slug=category_slug)

    search_query = request.GET.get('search')
    if search_query:
        posts = posts.filter(title__icontains=search_query) | posts.filter(description__icontains=search_query)

    # Pagination
    paginator = Paginator(posts, 6)  # 6 posts per page
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)  # <--- now posts is a Page object

    categories = Category.objects.all()

    context = {
        'posts': posts,  # template expects 'posts' for pagination
        'categories': categories,
        'selected_category': category_slug,
        'search_query': search_query,
    }
    return render(request, 'blog/home.html', context)



def post_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    related_posts = BlogPost.objects.filter(
        category=post.category, 
        is_published=True
    ).exclude(id=post.id)[:3]
    
    context = {
        'post': post,
        'related_posts': related_posts,
    }
    return render(request, 'blog/post_detail.html', context)

def subscribe_newsletter(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            newsletter, created = Newsletter.objects.get_or_create(email=email)
            if created:
                messages.success(request, 'Successfully subscribed to newsletter!')
            else:
                messages.info(request, 'You are already subscribed!')
        else:
            messages.error(request, 'Please provide a valid email address.')
    return redirect('home')


def about(request):
    categories = Category.objects.all()
    return render(request, 'blog/about.html', {'categories': categories})

def contact(request):
    categories = Category.objects.all()
    return render(request, 'blog/contact.html', {'categories': categories})


