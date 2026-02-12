from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
def index(request):
    return HttpResponse(
        "Rango says hey there partner! "
        "<br/>"
        "<a href='/rango/about/'>About</a>"
    )
from rango import views
urlpatterns = [
path('', views.index, name='index'),
path('admin/', admin.site.urls),
]
def about(request):
    return HttpResponse(
        "Rango says here is the about page."
        "<br/>"
        "<a href='/rango/'>Index</a>"
    )
