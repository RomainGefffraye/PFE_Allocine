import json, io, os
from collections import defaultdict
from all_class import *

def listdir_nohidden(path):
    for f in os.listdir(path):
        if not f.startswith('.'):
            yield f

def merge_data_from_crawl(): #To refactor far too long
    category_file = sorted(os.listdir(os.getcwd()+"/data/data_from_crawl"))
    movies_category = [file_name for file_name in category_file if not any(c.isdigit() for c in file_name)]
    for category in movies_category:
        if category.endswith('.json'):
            category = category[:-5]
        if category.endswith('die'):
            movies_with_part = [file_name for file_name in category_file if (len(file_name) < 30 and category in file_name)]
        else:
            movies_with_part = [file_name for file_name in category_file if category in file_name]
        if len(movies_with_part) > 1:
            all_part_data = {}
            for movies_part in movies_with_part:
                with open('data/data_from_crawl/' + movies_part) as part:
                    data = json.load(part)
                for movie_title, movie_data in data.iteritems():
                    all_part_data[movie_title] = movie_data
            with io.open("data/data_to_use/" + movies_with_part[0] , "w+", encoding='utf8') as all_part:
                output = json.dumps(all_part_data, ensure_ascii=False, encoding='utf8')
                all_part.write(unicode(output))
        if len(movies_with_part) == 1 and  movies_with_part[0][0] != '.':
            with open('data/data_from_crawl/' + movies_with_part[0]) as part:
                data = json.load(part)
            with io.open("data/data_to_use/" + movies_with_part[0] , "w+", encoding='utf8') as all_part:
                output = json.dumps(data, ensure_ascii=False, encoding='utf8')
                all_part.write(unicode(output))


def create_all_movies_file():
    all_data = {}
    for content in listdir_nohidden(os.getcwd() + "/data/data_to_use"):
        with open('data/data_to_use/' + content) as data_file:
            data = json.load(data_file)
            for movie_title, movie_data in data.iteritems():
                all_data[movie_title] = movie_data
    print "All data", len(all_data)
    with io.open("data/all_movies.json", "w+", encoding='utf8') as all_data_file:
        output = json.dumps(all_data, ensure_ascii=False, encoding='utf8')
        all_data_file.write(unicode(output))

def get_set_of_distributors(data):
    distributors = set()
    for movie_title, movie_data in data.iteritems():
        distributors.add(movie_data["distributor"])
    return distributors

def get_movies_per_years_per_distributors(set_distributors, data):
    json_data = {}
    for distributor in set_distributors:
        data_to_display = Movies_per_distributor_per_year(data, distributor)
        if data_to_display.relevant == True:
            json_data[data_to_display.distributor] = data_to_display.data_for_d3
    return json_data

def generate_data_d3(chart_name, data_name, chart_data):
    with io.open("d3_visualisation/data/" + chart_name, "w+", encoding='utf8') as js_file:
        js_file.write(u"var " + unicode(data_name) + u" = ")
        output = json.dumps(chart_data, ensure_ascii=False, encoding='utf8')
        js_file.write(unicode(output))

def generate_data_distributor_movies_year(chart_name, chart_data):
    with io.open("d3_visualisation/data/" + chart_name, "w+", encoding='utf8') as js_file:
        js_file.write(u"var genre_counter = ")
        output = json.dumps(chart_data, ensure_ascii=False, encoding='utf8')
        js_file.write(unicode(output))


def get_movie_distribution_distributor(data):
    movie_distribution = defaultdict(lambda: 0)
    for movie in data:
        if data[movie]["distributor"] is not None:
            movie_distribution[data[movie]["distributor"]] += 1
    return movie_distribution

def get_list_of_company(data):
    list_of_company = []
    distribution = get_movie_distribution_distributor(data)
    for movie in data:
        distributor = data[movie]["distributor"]
        if distributor not in list_of_company:
            if distribution[distributor] > 100:
                list_of_company.append(distributor)
    return list_of_company

def get_list_of_different_parameters(data):
    dict_of_list = {}
    set_of_genre = set()
    set_of_years = set()
    set_of_actors = set()
    set_of_realisators = set()
    set_of_distributors = set()
    for movie in data:
        for genre in data[movie]["genres"]:
            set_of_genre.add(genre)
        set_of_years.add(data[movie]["production_year"])
        set_of_distributors.add(data[movie]["distributor"])
        if data[movie]["actors"] != None:
            for actor in data[movie]["actors"]:
                set_of_actors.add(actor)
        if data[movie]["realisator"] != None:
            for realisator in data[movie]["realisator"]:
                set_of_realisators.add(realisator)
    dict_of_list["genres"] = [ x for x in iter(set_of_genre) ]
    dict_of_list["production_year"] = [ x for x in iter(set_of_years) ]
    dict_of_list["realisators"] = [ x for x in iter(set_of_realisators) ]
    dict_of_list["actors"] = [ x for x in iter(set_of_actors) ]
    dict_of_list["distributor"] = [ x for x in iter(set_of_distributors) ]
    return dict_of_list

def get_count_genres_and_actors(data):
    genres_number = defaultdict(int)
    actors_number = defaultdict(int)
    realisators_number = defaultdict(int)
    production_years_number = defaultdict(int)
    for movie in data:
        genres = data[movie]["genres"]
        if genres:
            for genre in genres:
                genres_number[genre] += 1
        actors = data[movie]["actors"]
        if actors:
            for actor in actors:
                actors_number[actor] += 1
        realisators = data[movie]["realisator"]
        if realisators:
            for realisator in realisators:
                realisators_number[realisator] += 1
        production_year = data[movie]["production_year"]
        if production_year:
            production_years_number[production_year] += 1
    return (genres_number, actors_number, realisators_number, production_years_number)

def get_data_formated_genre_bar(data_to_format, min_value):
    key = {}
    values = []
    key["key"] = "Nombre de films par genre"
    for genre, number in data_to_format.iteritems():
        bar = {}
        bar["label"] = genre
        bar["value"] = number
        values.append(bar)
    values = sorted(values, key=lambda k: k['value'], reverse=True)
    values = [x for x in values if x['value'] > min_value]
    key["values"] = values
    return key

def get_movie_distribution_distributor_year(data):
    movie_distribution = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0)))
    for movie in data:
        if len(data[movie]["genres"]) > 0:
            genre = data[movie]["genres"][0]
            distributor = data[movie]["distributor"]
            year = data[movie]["production_year"]
            movie_distribution[genre][distributor][year] += 1
    return movie_distribution

def get_movies_per_productor(data, list_of_parameter):
    children = []
    movie = {"name": "movie", "children": children}
    list_of_company = get_list_of_company(data)
    list_of_year = list_of_parameter["production_year"]
    list_of_genre = list_of_parameter["genres"]
    distribution = get_movie_distribution_distributor_year(data)
    for genre in list_of_genre:
        genre_distribution = {}
        genre_distribution["name"] = genre
        genre_distribution["children"] = []
        for company in list_of_company:
            company_distribution = {}
            company_distribution["name"] = company
            company_distribution["children"] = []
            for year in list_of_year:
                year_distribution = {}
                year_distribution["name"] = year
                year_distribution["size"] = distribution[genre][company][year]
                if distribution[company][year] > 0:
                    company_distribution["children"].append(year_distribution)
            genre_distribution["children"].append(company_distribution)
        children.append(genre_distribution)
    return(movie)
