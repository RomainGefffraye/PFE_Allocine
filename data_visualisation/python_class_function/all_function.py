import json, io, os
from all_class import *

def listdir_nohidden(path):
    for f in os.listdir(path):
        if not f.startswith('.') and not f == "all_movies.json":
            yield f

def create_all_movies_file():
    all_data = {}
    list_of_genre = []
    list_of_genre.append("Drame")
    for content in listdir_nohidden(os.getcwd() + "/data"):
        list_of_genre.append(content.rpartition("_")[2])
        with open('data/' + content) as data_file:
            data = json.load(data_file)
            for movie_title, movie_data in data.iteritems():
                all_data[movie_title] = movie_data
    with io.open("data/all_movies.json", "w+", encoding='utf8') as all_data_file:
        output = json.dumps(all_data, ensure_ascii=False, encoding='utf8')
        all_data_file.write(unicode(output))
    return list_of_genre


def get_set_of_distributors(data):
    distributors = set()
    for movie_title, movie_data in data.iteritems():
        distributors.add(movie_data["distributor"])
    return distributors


def get_movies_per_years_per_distributors(set_distributors, data):
    json_data = {}
    for distributor in set_distributors:
        data_to_display = Movies_per_distributor_per_year(data, distributor)
        json_data[data_to_display.distributor] = data_to_display.data_for_d3
    return json_data

def generate_data_d3(chart_name, chart_data):
    with io.open("d3_visualisation/" + chart_name, "w+", encoding='utf8') as js_file:
        js_file.write(u"var movies_per_years_per_distributor = ")
        output = json.dumps(chart_data, ensure_ascii=False, encoding='utf8')
        js_file.write(unicode(output))
