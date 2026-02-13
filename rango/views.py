from django.shortcuts import render, redirect, get_object_or_404
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm

def index(request):
    """Display the top 5 categories by likes and top 5 pages by views."""
    categories = Category.objects.order_by('-likes')[:5]
    top_pages = Page.objects.order_by('-views')[:5]

    context = {
        'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!',
        'categories': categories,
        'top_pages': top_pages
    }

    return render(request, 'rango/index.html', context)


def about(request):
    """Render the about page."""
    return render(request, 'rango/about.html')


def show_category(request, category_name_slug):
    """Display a single category and its pages."""
    category = get_object_or_404(Category, slug=category_name_slug)
    pages = Page.objects.filter(category=category)

    context = {
        'category': category,
        'pages': pages
    }
    return render(request, 'rango/category.html', context)


def add_category(request):
    """Handle adding a new category via a form."""
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            cat = form.save(commit=True)
            print(f'New Category Added: {cat.name} ({cat.slug})')
            return redirect('rango:index')
        else:
            print(form.errors)
    else:
        form = CategoryForm()

    return render(request, 'rango/add_category.html', {'form': form})


def add_page(request, category_name_slug):
    """Handle adding a new page to a specific category."""
    category = get_object_or_404(Category, slug=category_name_slug)

    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            page = form.save(commit=False)
            page.category = category
            page.save()
            return redirect('rango:show_category', category_name_slug=category.slug)
        else:
            print(form.errors)
    else:
        form = PageForm()

    context = {
        'form': form,
        'category': category
    }
    return render(request, 'rango/add_page.html', context)

