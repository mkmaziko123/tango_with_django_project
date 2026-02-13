from django.shortcuts import render
from rango.models import Category, Page

def index(request):
    """View for the main Rango page."""
    
    # Retrieve top 5 categories ordered by likes (descending)
    top_categories = Category.objects.order_by('-likes')[:5]

    # Retrieve top 5 pages ordered by views (descending)
    top_pages = Page.objects.order_by('-views')[:5]

    # Context dictionary to pass to template
    context_dict = {
        'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!',
        'categories': top_categories,
        'top_pages': top_pages
    }

    return render(request, 'rango/index.html', context=context_dict)


def about(request):
    """View for the About page."""
    return render(request, 'rango/about.html')


def show_category(request, category_name_slug):
    """View for a specific category and its pages."""
    
    context_dict = {}

    try:
        # Fetch the category using the slug
        category = Category.objects.get(slug=category_name_slug)

        # Get all pages for this category
        pages = Page.objects.filter(category=category)

        context_dict['category'] = category
        context_dict['pages'] = pages

    except Category.DoesNotExist:
        # Category not found
        context_dict['category'] = None
        context_dict['pages'] = None

    return render(request, 'rango/category.html', context=context_dict)

