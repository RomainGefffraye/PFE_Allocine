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
            return int(production_year[0].find("span", {"class" : "that"}).text.strip())
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

def crawl_from_save(movies_category):
    f = open("urls/progress/last_crawled", "r")
    last_url_crawled = f.readline()
    f.close()
    data_json = {}
    with open("urls/movies/" + movies_category) as movies_url:
        for movie in movies_url:
            while last_url_crawled.split() != movie.split():
                pass
        line_number = 0
        part_number = 0
        for movie in movies_url:
            line_number += 1
            if line_number % 5000 == 0:
                part_number += 1
                with open("data/movies_json/" + movies_category + "_" + part_number + ".json", 'w+') as data:
                    json.dump(data_json, data)
                with open("urls/progress/last_crawled", 'w+') as save:
                    write(movie, save)
                data_json = {}
            print movie[:-1]
            page = requests.get(movie, headers=headers)
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
            if line_number % 5000 == 0:
                part_number += 1
                with open("data/movies_json/" + movies_category + "_" + part_number + ".json", 'w+') as data:
                    json.dump(data_json, data)
                with open("urls/progress/last_crawled", 'w+') as save:
                    write(movie, save)
                data_json = {}
            print movie[:-1]
            page = requests.get(movie, headers=headers)
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

category_file = sorted(os.listdir(os.getcwd()+"/data/movies_url"))
for movies_category in category_file:
    if os.path.exists(os.getcwd()+"/urls/progress/last_crawled"):
        crawl_from_save(movies_category)
    else:
        crawl(movies_category)
    os.remove(os.getcwd() + "/urls/progress/last_crawled")
