from django.shortcuts import render
from searchpaper.forms import SearchForm

# Create your views here.


def search(request):
    context = {}
    if request.method == "GET":
        context['form'] = SearchForm()
        return render(request, 'searchpaper/search.html', context)

    form = SearchForm(request.POST)
    context['form'] = form

    if not form.is_valid():
        return render(request, 'searchpaper/search.html', context)

    return render(request, 'searchpaper/result.html', context) 


# def similarweb(google sheet):
# return total visit duration of different piracy sites 


# seilinum crawl aiyifan 火力值



# movie to overall streaming ratio: Aiyifan avengers moveis streaming volume / Aiyifan total streaming volume on Aiyifan


# gpt translate 
