import json, io, os
from collections import defaultdict
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

def getMovieDistributionDistributor(data):
    movieDistribution = defaultdict(lambda: 0)
    for movie in data:
        if data[movie]["distributor"] is not None:
            movieDistribution[data[movie]["distributor"]] += 1
    return movieDistribution

def getListOfCompany(data):
    listOfCompany = []
    distribution = getMovieDistributionDistributor(data)
    for movie in data:
        distributor = data[movie]["distributor"]
        if distributor not in listOfCompany:
            if distribution[distributor] > 100:
                listOfCompany.append(distributor)
    return listOfCompany

def getListOfYear(data):
    listOfYear = []
    for movie in data:
        if data[movie]["production_year"] not in listOfYear:
            listOfYear.append(data[movie]["production_year"])
    return listOfYear


def getListOfGenre(data):
    listOfGenre = []
    for movie in data:
        for genre in data[movie]["genres"]:
            if genre not in listOfGenre:
                listOfGenre.append(genre)
    return listOfGenre


def getMovieDistributionDistributorYear(data):
    movieDistribution = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0)))
    for movie in data:
        if len(data[movie]["genres"]) > 0:
            genre = data[movie]["genres"][0]
            distributor = data[movie]["distributor"]
            year = data[movie]["production_year"]
            movieDistribution[genre][distributor][year] += 1
    return movieDistribution



def getMoviesPerProductor(data):
    children = []
    movie = {"name": "movie", "children": children}
    #print(data["Zero"].keys())
    listOfCompany = getListOfCompany(data)
    listOfYear = getListOfYear(data)
    listOfGenre = getListOfGenre(data)[:17] #Need to fix the bug where there's actor inside "genres"
    distribution = getMovieDistributionDistributorYear(data)
    for genre in listOfGenre:
        genreDistribution = {}
        genreDistribution["name"] = genre
        genreDistribution["children"] = []
        for company in listOfCompany:
            companyDistribution = {}
            companyDistribution["name"] = company
            companyDistribution["children"] = []
            for year in listOfYear:
                yearDistribution = {}
                yearDistribution["name"] = year
                yearDistribution["size"] = distribution[genre][company][year]
                if distribution[company][year] > 0:
                    companyDistribution["children"].append(yearDistribution)
            genreDistribution["children"].append(companyDistribution)
        children.append(genreDistribution)
    return(movie)
