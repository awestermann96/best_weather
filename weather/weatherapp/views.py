from django.shortcuts import render
from .models import WeatherData
import json
import urllib.request

def home(request):
    return render(request, 'index.html')

# Create your views here.
def weather_list(request):
    weather = WeatherData.objects.all()[:9]
    return render(request, 'weather_list.html', {'weather_list': weather})

def result(request):
    words = request.GET['Region']
    return render(request, 'result.html', 
                  {'words': words})


from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import NameForm


def search(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect("/thanks/")

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, "home2.html", {"form": form})