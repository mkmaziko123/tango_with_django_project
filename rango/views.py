from django.shortcuts import render, redirect, get_object_or_404
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm
from django.shortcuts import render, redirect
from django.urls import reverse
from rango.forms import UserForm, UserProfileForm
from django.contrib.auth.decorators import login_required


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

@login_required
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



@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    # Cannot add a page to a non-existent category
    if category is None:
        return redirect('rango:index')

    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            page = form.save(commit=False)
            page.category = category
            page.views = 0
            page.save()
            return redirect(reverse('rango:show_category',
                                    kwargs={'category_name_slug': category.slug}))
        else:
            print(form.errors)

    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context_dict)
def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)  # Hash the password
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'rango/register.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'registered': registered
    })
def user_login(request):
    if request.method == 'POST':
        # Get username and password from the form
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate user
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('rango:index'))
            else:
                return HttpResponse("Your account is disabled.")
        else:
            print(f"Invalid login: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'rango/login.html')
@login_required
def restricted(request):
    return render(request, 'rango/restricted.html')
@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('rango:index'))

