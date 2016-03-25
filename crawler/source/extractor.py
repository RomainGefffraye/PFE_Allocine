from bs4 import BeautifulSoup
import os
import json
import requests
import re
import urlparse
import shutil

def load_save():
    f = open("urls/progress/last_crawled", "r")
    last_url_crawled = f.readline()
    f.close()
    flag = False
    file_to_continue = sorted(os.listdir(os.getcwd() + "/urls/pages"))[0]
    with open("urls/pages/" + file_to_continue) as pages_to_crawl:
        for line in pages_to_crawl:
            if flag:
                get_movies_URL(line, file_to_continue)
                print line
                with open ("urls/progress/last_crawled", "w+") as save:
                    save.write(line)
            if line == last_url_crawled:
                flag = True
    os.remove(file_to_continue)
    print "file " + file_to_continue + " deleted"

def get_categories():
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'
    }
    URL = "http://www.allocine.fr"
    page = requests.get(URL + "/films/", headers=headers)
    page_content = BeautifulSoup(page.content, 'html.parser')
    piece_HTML = page_content.findAll("div", { "class" : "left_col_menu_item" })
    return piece_HTML[0].findAll('a')

def generate_urls_pages_listing(categories):
    URL = "http://www.allocine.fr"
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'
    }
    pages_to_crawl = []
    for category in categories:
        URL_category = URL + category['href']
        page_category = requests.get(URL_category, headers=headers)
        page_category_content = BeautifulSoup(page_category.content, 'html.parser')
        div_button = page_category_content.findAll("div", { "class" : "pager navbar margin_20t" })
        if len(div_button) != 0:
            pages_button = div_button[0].findAll('li')
            pages_to_crawl.append((URL_category, category.text, int(pages_button[-1].text)))
        else:
            pages_to_crawl.append((URL_category, category.text, int(1)))
    for page_to_crawl in pages_to_crawl:
        with open("urls/pages/pages_" + page_to_crawl[1], 'w') as outfile:
            for page_number in range(1, page_to_crawl[2] + 1):
                outfile.write(page_to_crawl[0] + "?page=" + str(page_number) + "\n")

def get_movies_URL(URLs_page, pages_to_crawl):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'
    }
    main_URL = "http://www.allocine.fr"
    page = requests.get(URLs_page, headers=headers)
    page_content = BeautifulSoup(page.content, 'html.parser')
    movies = page_content.findAll("a", {"class" : "no_underline"})
    with open("urls/movies/movies_" + pages_to_crawl, "a") as myfile:
        for movie in movies:
            myfile.write(main_URL + movie['href'] + "\n")

def generate_urls_movie_listing():
    for pages_to_crawl in sorted(os.listdir(os.getcwd()+"/urls/pages")):
        print pages_to_crawl
        with open("urls/pages/" + pages_to_crawl) as f:
            for line in f:
                get_movies_URL(line, pages_to_crawl)
                print line
                with open("urls/progress/last_crawled", "w") as save:
                    save.write(line)
        os.remove(os.getcwd() + "/urls/pages/" + pages_to_crawl)
        print "File " + pages_to_crawl + " deleted"

pages_files = sorted(os.listdir(os.getcwd()+"/urls/pages"))
if not pages_files:
    generate_urls_pages_listing(get_categories())
if os.path.exists(os.getcwd()+"/urls/progress/last_crawled"):
    load_save()
    generate_urls_movie_listing()
else:
    generate_urls_movie_listing()
os.remove(os.getcwd() + "/urls/progress/last_crawled")
