#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import os
import json
import requests
import re
import urlparse
import shutil
import time

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
        production_year = filter((lambda x: x.find("span", { "class" : "what light"}).text == "Année de production".decode('UTF-8')), technical_info)
        if production_year:
            return production_year[0].find("span", {"class" : "that"}).text.strip()
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
        rate_value = filter((lambda x: x.find("span" ,{"class" : "rating-title blue-link"}) != None), all_rates)
        rate = filter((lambda x: x.find("span" ,{"class" : "rating-title blue-link"})['title'] == entity), rate_value)
        if rate:
            return float(rate[0].find("span", {"class" : "stareval-note"}).text.replace(',', '.'))
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
        list_of_realisator_link = informations[1].findAll("span", {"itemprop" : "name"})
        if list_of_realisator_link:
            return [realisator.text for realisator in list_of_realisator_link]
        else:
            return None

    def get_actors(self, general_info):
        informations = general_info.findAll("div", {"class" : "meta-body-item"})
        list_of_actor_link = informations[2].findAll("span", {"class" : "blue-link"})
        if list_of_actor_link:
            return [actor.text for actor in list_of_actor_link[:-1]]
        else:
            return None

    def get_genres(self, general_info):
        informations = general_info.findAll("div", {"class" : "meta-body-item"})
        list_of_genre = informations[3].findAll("span", {"class" : "blue-link"})
        return [genre.text for genre in list_of_genre]
        if list_of_genre:
            return [genre.text for genre in list_of_genre]
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



headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'
}
"""url = "http://www.allocine.fr/film/fichefilm_gen_cfilm=223207.html"
page = requests.get(url, headers=headers)
page_content = BeautifulSoup(page.content, 'html.parser')
movie = Movie(page_content, url)
movie.display()
data = movie.to_json({})
with open("test.json", 'w+') as my_test:
    json.dump(data, my_test)
url = "http://www.allocine.fr/film/fichefilm_gen_cfilm=215143.html"
page = requests.get(url, headers=headers)
page_content = BeautifulSoup(page.content, 'html.parser')
movie = Movie(page_content, url)
movie.display()
data = movie.to_json(data)"""


movies_files = sorted(os.listdir(os.getcwd()+"/data/movies_url"))
for movies in movies_files:
    data_json = {}
    with open("urls/movies/" + movies) as movies_url:
        for movie in movies_url:
            print movie[:-1]
            time.sleep(3)
            page = requests.get(movie, headers=headers)
            print page.status_code
            if page.status_code == 200:
                page_content = BeautifulSoup(page.content, 'html.parser')
                movie_crawled = Movie(page_content, movie[:-1])
                data_json = movie_crawled.to_json(data_json)
            else:
                print movie[:-1], page.status_code
    with open("data/movies_json/" + movies, 'w+') as my_test:
        json.dump(data_json, my_test)
    with open("urls/progress/last_crawled", "w") as save:
        save.write(movies)
