#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from bs4 import BeautifulSoup
import os
import json
import requests
import re
import urlparse
import shutil
import sys

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

class Extractor_test(unittest.TestCase):
    def test_terre(self):
        page = open("data/test_terre.html", 'r').read()
        url = "http://www.allocine.fr/film/fichefilm_gen_cfilm=13131.html"
        page_content = BeautifulSoup(page, 'html.parser')
        movie = Movie(page_content, url)
        self.assertEqual(movie.original_movie_title, "Terra estrangeira")
        self.assertEqual(movie.critic_rate, 2)
        self.assertEqual(movie.movie_title.encode("utf-8"), "Terre lointaine")
        self.assertEqual(movie.spectator_rate, 3.1)
        self.assertEqual(movie.genres[0], "Aventure")
        self.assertEqual(movie.actors, ["Fernando Alves Pinto", "Alexandre Borges", "Laura Cardoso"])
        self.assertEqual(movie.realisator, ["Walter Salles", "Daniela Thomas"])
        self.assertEqual(movie.production_year, 1995)
        self.assertEqual(movie.distributor.encode("utf-8"), '-')
        self.assertEqual(movie.budget, '-')
        self.assertEqual(movie.summary.split()[0].encode("utf-8"), "A")
        self.assertEqual(movie.url, url)
        self.assertEqual(movie.language.encode('utf-8'), "Portugais")

    def test_antonio(self):
        page = open("data/test_antonio.html", 'r').read()
        url = "http://www.allocine.fr/film/fichefilm_gen_cfilm=20101.html"
        page_content = BeautifulSoup(page, 'html.parser')
        movie = Movie(page_content, url)
        self.assertEqual(movie.original_movie_title, "Il Bel Antonio")
        self.assertEqual(movie.critic_rate, 4)
        self.assertEqual(movie.movie_title.encode("utf-8"), "Le Bel Antonio")
        self.assertEqual(movie.spectator_rate, 3.4)
        self.assertEqual(movie.genres[0].encode("utf-8"), "Comédie dramatique")
        self.assertEqual(movie.actors, ["Claudia Cardinale", "Marcello Mastroianni", "Pierre Brasseur"])
        self.assertEqual(movie.realisator, ["Mauro Bolognini"])
        self.assertEqual(movie.production_year, 1960)
        self.assertEqual(movie.distributor.encode("utf-8"), '-')
        self.assertEqual(movie.budget, '-')
        self.assertEqual(movie.summary.split()[0].encode("utf-8"), "Toutes")
        self.assertEqual(movie.url, url)
        self.assertEqual(movie.language.encode('utf-8'), "Italien")

    def test_legende_montagne(self):
        page = open("data/test_legende.html", 'r').read()
        url = "http://www.allocine.fr/film/fichefilm_gen_cfilm=112143.html"
        page_content = BeautifulSoup(page, 'html.parser')
        movie = Movie(page_content, url)
        self.assertEqual(movie.original_movie_title, "The Princess Stallion")
        self.assertEqual(movie.critic_rate, None)
        self.assertEqual(movie.movie_title.encode("utf-8"), "La légende des montagnes du Nord")
        self.assertEqual(movie.spectator_rate, None)
        self.assertEqual(movie.genres, ["Fantastique"])
        self.assertEqual(movie.actors, ["Ariana Richards", "Andrew Keir", "David Robb"])
        self.assertEqual(movie.realisator, ["Mark Haber"])
        self.assertEqual(movie.production_year, 1997)
        self.assertEqual(movie.distributor, '-')
        self.assertEqual(movie.budget, '-')
        self.assertEqual(movie.summary.split()[0].encode("utf-8"), "Après")
        self.assertEqual(movie.url, url)
        self.assertEqual(movie.language, "Anglais")

    def test_equilibrium(self):
        page = open("data/test_equilibrium.html", 'r').read()
        url = "http://www.allocine.fr/film/fichefilm_gen_cfilm=26865.html"
        page_content = BeautifulSoup(page, 'html.parser')
        movie = Movie(page_content, url)
        self.assertEqual(movie.original_movie_title, None)
        self.assertEqual(movie.critic_rate, 2.9)
        self.assertEqual(movie.movie_title.encode("utf-8"), "Equilibrium")
        self.assertEqual(movie.spectator_rate, 3.7)
        self.assertEqual(movie.genres, ["Science fiction", "Action", "Thriller"])
        self.assertEqual(movie.actors, ["Christian Bale", "Emily Watson", "Taye Diggs"])
        self.assertEqual(movie.realisator, ["Kurt Wimmer"])
        self.assertEqual(movie.production_year, 2002)
        self.assertEqual(movie.distributor.encode("utf-8"), 'TFM Distribution')
        self.assertEqual(movie.budget, '20 000 000 $')
        self.assertEqual(movie.summary.split()[0].encode("utf-8"), "Dans")
        self.assertEqual(movie.url, url)
        self.assertEqual(movie.language, "Anglais")

    def test_batman(self):
        page = open("data/test_batman.html", 'r').read()
        url = "http://www.allocine.fr/film/fichefilm_gen_cfilm=115362.html"
        page_content = BeautifulSoup(page, 'html.parser')
        movie = Movie(page_content, url)
        self.assertEqual(movie.original_movie_title, "The Dark Knight")
        self.assertEqual(movie.critic_rate, 4.0)
        self.assertEqual(movie.movie_title.encode("utf-8"), "The Dark Knight, Le Chevalier Noir")
        self.assertEqual(movie.spectator_rate, 4.6)
        self.assertEqual(movie.genres, ["Action", "Drame", "Thriller"])
        self.assertEqual(movie.actors, ["Christian Bale", "Heath Ledger", "Aaron Eckhart"])
        self.assertEqual(movie.realisator, ["Christopher Nolan"])
        self.assertEqual(movie.production_year, 2008)
        self.assertEqual(movie.distributor.encode("utf-8"), 'Warner Bros. France')
        self.assertEqual(movie.budget, '180 000 000 $')
        self.assertEqual(movie.summary.split()[0].encode("utf-8"), "Dans")
        self.assertEqual(movie.url, url)
        self.assertEqual(movie.language, "Anglais")

    def test_ping_pong(self):
        page = open("data/test_ping_pong.html", 'r').read()
        url = "http://www.allocine.fr/film/fichefilm_gen_cfilm=111362.html"
        page_content = BeautifulSoup(page, 'html.parser')
        movie = Movie(page_content, url)
        self.assertEqual(movie.original_movie_title, None)
        self.assertEqual(movie.critic_rate, 4.0)
        self.assertEqual(movie.movie_title.encode("utf-8"), "Pingpong")
        self.assertEqual(movie.spectator_rate, 3.0)
        self.assertEqual(movie.genres, ["Drame"])
        self.assertEqual(movie.actors, ["Sebastian Urzendowsky", "Marion Mitterhammer", "Clemens Berg"])
        self.assertEqual(movie.realisator, ["Matthias Luthardt"])
        self.assertEqual(movie.production_year, 2006)
        self.assertEqual(movie.distributor.encode("utf-8"), 'Les Acacias')
        self.assertEqual(movie.budget, '-')
        self.assertEqual(movie.summary.split()[0].encode("utf-8"), "Paul,")
        self.assertEqual(movie.url, url)
        self.assertEqual(movie.language, "Allemand")

    def test_iron_man(self):
        page = open("data/test_iron_man.html", 'r').read()
        url = "http://www.allocine.fr/film/fichefilm_gen_cfilm=139589.html"
        page_content = BeautifulSoup(page, 'html.parser')
        movie = Movie(page_content, url)
        self.assertEqual(movie.original_movie_title, None)
        self.assertEqual(movie.critic_rate, 3.2)
        self.assertEqual(movie.movie_title.encode("utf-8"), "Iron Man 3")
        self.assertEqual(movie.spectator_rate, 4.1)
        self.assertEqual(movie.genres, ["Action", "Science fiction"])
        self.assertEqual(movie.actors, ["Robert Downey Jr.", "Gwyneth Paltrow", "Don Cheadle"])
        self.assertEqual(movie.realisator, ["Shane Black"])
        self.assertEqual(movie.production_year, 2013)
        self.assertEqual(movie.distributor.encode("utf-8"), 'The Walt Disney Company France')
        self.assertEqual(movie.budget, '200 000 000 $')
        self.assertEqual(movie.summary.split()[0].encode("utf-8"), "Tony")
        self.assertEqual(movie.url, url)
        self.assertEqual(movie.language, "Anglais")


    def test_danger(self):
        page = open("data/test_danger.html", 'r').read()
        url = "http://www.allocine.fr/film/fichefilm_gen_cfilm=30624.html"
        page_content = BeautifulSoup(page, 'html.parser')
        movie = Movie(page_content, url)
        self.assertEqual(movie.original_movie_title, "Clear and Present Danger")
        self.assertEqual(movie.critic_rate, None)
        self.assertEqual(movie.movie_title.encode("utf-8"), "Danger immédiat")
        self.assertEqual(movie.spectator_rate, 3.0)
        self.assertEqual(movie.genres, ["Action", "Thriller"])
        self.assertEqual(movie.actors, ["Harrison Ford", "Willem Dafoe", "Anne Archer"])
        self.assertEqual(movie.realisator, ["Phillip Noyce"])
        self.assertEqual(movie.production_year, 1994)
        self.assertEqual(movie.distributor.encode("utf-8"), 'United International Pictures (UIP)')
        self.assertEqual(movie.budget, '65 000 000 $')
        self.assertEqual(movie.summary.split()[0].encode("utf-8"), "Après")
        self.assertEqual(movie.url, url)
        self.assertEqual(movie.language, "Anglais")

    def test_german(self):
        page = open("data/test_german.html", 'r').read()
        url = "http://www.allocine.fr/film/fichefilm_gen_cfilm=221473.html"
        page_content = BeautifulSoup(page, 'html.parser')
        movie = Movie(page_content, url)
        self.assertEqual(movie.original_movie_title, None)
        self.assertEqual(movie.critic_rate, None)
        self.assertEqual(movie.movie_title.encode("utf-8"), "German Angst")
        self.assertEqual(movie.spectator_rate, 3.0)
        self.assertEqual(movie.genres, ["Epouvante-horreur", "Action"])
        self.assertEqual(movie.production_year, 2015)
        self.assertEqual(movie.distributor.encode("utf-8"), '-')
        self.assertEqual(movie.budget, '-')
        self.assertEqual(movie.summary, None)
        self.assertEqual(movie.url, url)
        self.assertEqual(movie.language, "Anglais, Allemand, Polonais, ukrainien, Italien")

    def test_oranais(self):
        page = open("data/test_oranais.html", 'r').read()
        url = "http://www.allocine.fr/film/fichefilm_gen_cfilm=215342.html"
        page_content = BeautifulSoup(page, 'html.parser')
        movie = Movie(page_content, url)
        self.assertEqual(movie.original_movie_title, None)
        self.assertEqual(movie.critic_rate, 3.5)
        self.assertEqual(movie.movie_title.encode("utf-8"), "L'Oranais")
        self.assertEqual(movie.spectator_rate, 3.8)
        self.assertEqual(movie.genres, ["Drame", "Historique"])
        self.assertEqual(movie.actors, ["Lyes Salem", "Khaled Benaissa", "Djemel Barek"])
        self.assertEqual(movie.realisator, ["Lyes Salem"])
        self.assertEqual(movie.production_year, 2013)
        self.assertEqual(movie.distributor.encode("utf-8"), 'Haut et Court')
        self.assertEqual(movie.budget, '-')
        self.assertEqual(movie.summary.split()[0].encode("utf-8"), "Durant")
        self.assertEqual(movie.url, url)
        self.assertEqual(movie.language.encode('utf-8'), "Français")

    def test_eternal(self):
        page = open("data/test_eternal.html", 'r').read()
        url = "http://www.allocine.fr/film/fichefilm_gen_cfilm=186635.html"
        page_content = BeautifulSoup(page, 'html.parser')
        movie = Movie(page_content, url)
        self.assertEqual(movie.original_movie_title, None)
        self.assertEqual(movie.critic_rate, None)
        self.assertEqual(movie.movie_title.encode("utf-8"), "Eternal")
        self.assertEqual(movie.spectator_rate, None)
        self.assertEqual(movie.genres, ["Drame", "Fantastique"])
        self.assertEqual(movie.actors, None)
        self.assertEqual(movie.realisator, ["Paul Verhoeven"])
        self.assertEqual(movie.production_year, None)
        self.assertEqual(movie.distributor.encode("utf-8"), '-')
        self.assertEqual(movie.budget, '-')
        self.assertEqual(movie.summary.split()[0].encode("utf-8"), "Alors")
        self.assertEqual(movie.url, url)
        self.assertEqual(movie.language.encode('utf-8'), "Anglais")


if __name__ == '__main__':
    suite = unittest.TestSuite()
    tests = unittest.defaultTestLoader.loadTestsFromTestCase(Extractor_test)
    suite.addTests(tests)
    unittest.TextTestRunner().run(suite)
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:2.0.1) Gecko/20100101 Firefox/4.0.1'
    }
