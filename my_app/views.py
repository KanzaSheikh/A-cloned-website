from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from requests.compat import quote_plus
from . import models

#BASE_CRAIGSLIST_URL = "https://losangeles.craigslist.org/search/?query={}"
#BASE_CRAIGSLIST_URL = "https://ahmedabad.craigslist.org/search/?query={}"
#BASE_CRAIGSLIST_URL = "https://www.google.com/search?safe=active&sxsrf=ALeKk02Zq9U1aBWyT98PLRmzlTIBqh1itQ%3A1589387675518&source=hp&ei=myG8XtSxHcyXlwT0v7_IBw&q={}&oq={}&gs_lcp=CgZwc3ktYWIQAzIFCAAQkQIyAggAMgIIADICCAAyAggAMgIIADICCAAyAggAMgIIADICCAA6BAgjECc6CAgAEJECEIsDOggIABCDARCLAzoFCAAQiwM6BAgAEEM6BQgAEIMBOgcIABBDEIsDOgcIIxCxAhAnOgQIABAKULoPWPsvYJQ5aANwAHgBgAGQBYgB5iqSAQkyLTQuNC40LjKYAQCgAQGqAQdnd3Mtd2l6uAEC&sclient=psy-ab&ved=0ahUKEwiU67q-orHpAhXMy4UKHfTfD3kQ4dUDCAc&uact=5"
#BASE_CRAIGSLIST_URL = "https://poets.org/search?combine={}"
BASE_CRAIGSLIST_URL = "https://www.poetryfoundation.org/search?query={}"
BASE_SEARCH_URL = "https://www.poetryfoundation.org{}"

# Create your views here.

def home(request):
    return render(request, 'base.html')

def new_search(request):
    search = request.POST.get('search')
    models.Search.objects.create(search=search)
    print(quote_plus(search))
    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(search))
    print(final_url)
    response = requests.get(final_url)
    #response = requests.get("https://www.google.com/search?safe=active&sxsrf=ALeKk02Zq9U1aBWyT98PLRmzlTIBqh1itQ%3A1589387675518&source=hp&ei=myG8XtSxHcyXlwT0v7_IBw&q=hello+world&oq=hello+world&gs_lcp=CgZwc3ktYWIQAzIFCAAQkQIyAggAMgIIADICCAAyAggAMgIIADICCAAyAggAMgIIADICCAA6BAgjECc6CAgAEJECEIsDOggIABCDARCLAzoFCAAQiwM6BAgAEEM6BQgAEIMBOgcIABBDEIsDOgcIIxCxAhAnOgQIABAKULoPWPsvYJQ5aANwAHgBgAGQBYgB5iqSAQkyLTQuNC40LjKYAQCgAQGqAQdnd3Mtd2l6uAEC&sclient=psy-ab&ved=0ahUKEwiU67q-orHpAhXMy4UKHfTfD3kQ4dUDCAc&uact=5")
    #response = requests.get("https://ahmedabad.craigslist.org/search/bbb?query=python%20tutor&sort=rel")
    #response = requests.get("https://losangeles.craigslist.org/search/bbb?query=python%20tutor&sort=rel")
    #response = requests.get("https://poets.org/search?combine=daffodils")
    #response = requests.get("https://www.poetryfoundation.org/search?query=Daffodils")
    data = response.text
    soup = BeautifulSoup(data, 'html.parser')
    #print(soup.prettify())
    #print(soup.get_text())
    #post_titles = soup.find_all('a', {'class': 'result-title'})
    post_listings = soup.find_all('div', {'class': 'c-feature'})
    #post_listings = soup.find_all('li', {'class': 'result-row'})
    #post_titles = soup.find_all('a')
    #print(post_listings[0].text)
    '''print(post_listings[0].find(class_='c-txt').text)
    print(post_listings[0].find('a').get('href'))
    print(post_listings[0].find('a').text)
    print(post_listings[0].find(class_='c-txt_attribution').text)
    print(post_listings[0].find('p').text)'''
    #title1 = soup.title
    #print(title1)
    #print(data)
    final_postings = []
    for post in post_listings:
        if post.find(class_='c-txt'):
            post_tag = post.find(class_='c-txt').text
        else:
            post_tag = "N/A"
        if post.find('a'):
            post_title = post.find('a').text
        else:
            post_title = "N/A"
        if post.find('a'):
            post_url_id = post.find('a').get('href')  
            post_url = BASE_SEARCH_URL.format(post_url_id) 
        else:
            post_url = "#"
        if post.find(class_='c-txt_attribution'):
            post_writer = post.find(class_='c-txt_attribution').text
        else:
            post_writer = "N/A"
        if post.find('p'):
            post_description = post.find('p').text
        else:
            post_description = "N/A"
        if post.find('img'):
            post_image_url = post.find('img').get('srcset').split(',')[0]
            print(post_image_url)
        else:
            post_image_url = "data:image/jpeg;base64,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"  
        final_postings.append((post_tag, post_title, post_url, post_writer, post_description, post_image_url))
    stuff_for_frontend = {
        'search': search,
        'final_postings': final_postings,
    }
    return render(request, 'my_app/new_search.html', stuff_for_frontend)