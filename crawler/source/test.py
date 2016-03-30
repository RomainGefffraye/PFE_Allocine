#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import os, io
import json
import requests
import re
import urlparse
import shutil
import time
import random

class Movie:
    def to_json(self, data):
        json_movie = {}
        for attr, value in self.__dict__.iteritems():
            if attr == 'movie_title':
                pass
            else:
                if value == "-":
                    json_movie[attr] = None
                else:
                    json_movie[attr] = value
        data[self.movie_title] = json_movie
        return data

    def get_movie_title(self, movie_html):
        title = movie_html.findAll("div", { "class" : "titlebar-title titlebar-title-lg"})
        return title[0].text.strip()


    def get_movie_original_title(self, movie_html):
        technical_info = movie_html.findAll("div", { "class" : "item"})
        original_title = filter((lambda x: x.find("span", { "class" : "what light"}).text == " Titre original "), technical_info)
        if original_title:
            return original_title[0].find("span", {"class" : "that"}).text.strip()
        else:
            return None

    def get_distributor(self, movie_html):
        technical_info = movie_html.findAll("div", { "class" : "item"})
        distributor = filter((lambda x: x.find("span", { "class" : "what light"}).text == "Distributeur"), technical_info)
        if distributor:
            return distributor[0].find("span", {"class" : "that"}).text.strip()
        else:
            return None

    def get_production_year(self, movie_html):
        technical_info = movie_html.findAll("div", { "class" : "item"})
        production_year_tag = filter((lambda x: x.find("span", { "class" : "what light"}).text == "Année de production".decode('UTF-8')), technical_info)
        production_year = production_year_tag[0].find("span", {"class" : "that"}).text.strip()
        if production_year:
            return int(production_year)
        else:
            return None

    def get_language(self, movie_html):
        technical_info = movie_html.findAll("div", { "class" : "item"})
        language = filter((lambda x: x.find("span", { "class" : "what light"}).text == "Langues"), technical_info)
        if language:
            return language[0].find("span", {"class" : "that"}).text.strip()
        else:
            return None

    def get_budget(self, movie_html):
        technical_info = movie_html.findAll("div", { "class" : "item"})
        budget = filter((lambda x: x.find("span", { "class" : "what light"}).text == "Budget"), technical_info)
        if budget:
            return budget[0].find("span", {"class" : "that"}).text.strip()
        else:
            return None

    def get_rate(self, movie_html, entity):
        all_rates = movie_html.findAll("div", { "class" : "rating-item"})[:-1]
        rate_string = None
        for rate in all_rates:
            if entity[:4].lower() in rate.find("span", {"class" : "rating-title"}).text.strip().lower():
                rate_string = rate.find("span", {"class" : "stareval-note"}).text
        if rate_string and rate_string != "?":
            return float(rate_string.replace(',', '.'))
        else:
            return None

    def get_summary(self, movie_html):
        summary = movie_html.find("div", { "class" : "ovw-synopsis-txt"})
        if summary == None:
            return None
        else:
            return summary.text.strip()

    def get_realisator(self, general_info):
        informations = general_info.findAll("div", {"class" : "meta-body-item"})
        for information in informations:
            realisator_category = information.find("span", {"class" : "light"})
            if "de" in realisator_category.text.lower():
                realisators = information.findAll("span", {"itemprop" : "name"})
        if realisators:
            return [realisator.text for realisator in realisators]
        else:
            return None

    def get_actors(self, general_info):
        informations = general_info.findAll("div", {"class" : "meta-body-item"})
        for information in informations:
            actors_category = information.find("span", {"class" : "light"})
            if "avec" in actors_category.text.lower():
                actors = information.findAll("span", {"class" : "blue-link"})
        if actors:
            return [actor.text.strip() for actor in actors[:-1]]
        else:
            return None

    def get_genres(self, general_info):
        informations = general_info.findAll("div", {"class" : "meta-body-item"})
        for information in informations:
            genre_category = information.find("span", {"class" : "light"})
            if "genre" in genre_category.text.lower():
                genres = information.findAll("span", {"itemprop" : "genre"})
        if genres:
            return [genre.text for genre in genres]
        else:
            return None

    def __init__(self, page_content, url):
        general_info = page_content.find("div", { "class" : "meta__body"})
        if not general_info:
            general_info = page_content.find("div", { "class" : "meta-body"})
        self.url = url
        self.spectator_rate = self.get_rate(page_content, "Spectateurs")
        self.critic_rate = self.get_rate(page_content, "Presse")
        self.movie_title = self.get_movie_title(page_content)
        self.original_movie_title = self.get_movie_original_title(page_content)
        self.distributor = self.get_distributor(page_content)
        self.production_year = self.get_production_year(page_content)
        self.language = self.get_language(page_content)
        self.budget = self.get_budget(page_content)
        self.summary = self.get_summary(page_content)
        self.realisator = self.get_realisator(general_info)
        self.genres = self.get_genres(general_info)
        self.actors = self.get_actors(general_info)

    def display(self):
        print "Titre: ", self.movie_title
        print "Titre originale: ", self.original_movie_title
        print "Distributeur: ", self.distributor
        print "Annee de production: ", self.production_year
        print "Langue: ", self.language
        print "Budget: ", self.budget
        print "Resume: ", self.summary
        print "Realisator: ", self.realisator
        print "Acteurs: ", self.actors
        print "Genre: ", self.genres
        print "Note spectateur: ", self.spectator_rate
        print "Note presse: ", self.critic_rate
        print "Lien: ", self.url

def get_last_part_number(movies_category):
    category_file = sorted(os.listdir(os.getcwd()+"/data/movies_json"))
    movies_with_part = [file_name for file_name in category_file if any(c.isdigit() for c in file_name)]
    movies_categorty_with_part = [file_name for file_name in movies_with_part if movies_category in file_name]
    last_part = 0
    for file_name in movies_categorty_with_part:
        part = int(filter(str.isdigit, file_name))
        if part > last_part:
            last_part = part
    return last_part


def crawl_from_save(movies_category):
    f = open("progress/last_crawled", "r")
    last_url_crawled = f.readline()
    f.close()
    data_json = {}
    with open("urls/movies/" + movies_category) as movies_url:
        for movie in movies_url:
            if movie.strip() == last_url_crawled.strip():
                break
        line_number = 0
        part_number = get_last_part_number(movies_category)
        print part_number
        for movie in movies_url:
            line_number += 1
            if line_number % 4000 == 0:
                part_number += 1
                with open("data/movies_json/" + movies_category + "_" + str(part_number) + ".json", 'w+') as data:
                    json.dump(data_json, data)
                with open("progress/last_crawled", 'w+') as save:
                    save.write(movie)
                data_json = {}
            print movie[:-1]
            page = requests.get(movie, headers=random.choice(list_headers))
            if page.status_code == 200:
                page_content = BeautifulSoup(page.content, 'html.parser')
                movie_crawled = Movie(page_content, movie[:-1])
                data_json = movie_crawled.to_json(data_json)
            else:
                print movie[:-1], page.status_code
    with open("data/movies_json/" + movies_category + ".json", 'w+') as my_test:
        json.dump(data_json, my_test)


def crawl(movies_category):
    data_json = {}
    with open("urls/movies/" + movies_category) as movies_url:
        line_number = 0
        part_number = 0
        for movie in movies_url:
            line_number += 1
            if line_number % 4000 == 0:
                part_number += 1
                with open("data/movies_json/" + movies_category + "_" + str(part_number) + ".json", 'w+') as data:
                    json.dump(data_json, data)
                with open("progress/last_crawled", 'w+') as save:
                    save.write(movie)
                data_json = {}
            print movie[:-1]
            page = requests.get(movie, headers=random.choice(list_headers))
            if page.status_code == 200:
                page_content = BeautifulSoup(page.content, 'html.parser')
                movie_crawled = Movie(page_content, movie[:-1])
                data_json = movie_crawled.to_json(data_json)
            else:
                print movie[:-1], page.status_code
    with open("data/movies_json/" + movies_category + ".json", 'w+') as my_test:
        json.dump(data_json, my_test)


headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'
}

list_headers = [{
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'
}, {'User-Agent': 'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.7.6) Gecko/20050512 Firefox'
}, {'User-Agent': 'Mozilla/5.0 (Macintosh; U; PPC Mac OS X Mach-O; en-US; rv:1.7.12) Gecko/20050915 Firefox/1.0.7'
}, {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.27 Safari/525.13'
}, {'User-Agent': 'Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/4.0.202.0 Safari/532.0'
}, {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0'
}, {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)'}]

category_file = sorted(os.listdir(os.getcwd()+"/data/movies_url"))
for movies_category in category_file:
    get_last_part_number(movies_category)
    if os.path.exists(os.getcwd()+"/progress/last_crawled"):
        crawl_from_save(movies_category)
    else:
        crawl(movies_category)
    if os.path.exists(os.getcwd()+"/progress/last_crawled"):
        os.remove(os.getcwd() + "/progress/last_crawled")

category_file = sorted(os.listdir(os.getcwd()+"/data/movies_json"))
movies_category = [file_name for file_name in category_file if not any(c.isdigit() for c in file_name)]
for category in movies_category:
    if category.endswith('.json'):
        category = category[:-5]
    if category.endswith('die'):
        movies_with_part = [file_name for file_name in category_file if (len(file_name) < 28 and category in file_name)]
    else:
        movies_with_part = [file_name for file_name in category_file if category in file_name]
    if len(movies_with_part) > 1:
        all_movies = {}
        for movies_part in movies_with_part:
            with open('data/movies_json/' + movies_part) as part:
                all_movies = json.load(part)
        with io.open("data/movies_json/" + movies_with_part[0][:-5] + "_all_part.json" , "w+", encoding='utf8') as all_part:
            output = json.dumps(all_movies, ensure_ascii=False, encoding='utf8')
            all_part.write(unicode(output))
