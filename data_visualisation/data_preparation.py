from python_class_function.all_function import *

merge_data_from_crawl()

create_all_movies_file()

with open(os.getcwd()+"/data/all_movies.json", ) as data_file:
    data = json.load(data_file)

list_of_parameters = get_list_of_different_parameters(data)
with open('d3_visualisation/data/sunburst.json', 'w') as fp:
    json.dump(get_movies_per_productor(data, list_of_parameters), fp)

distributors = get_set_of_distributors(data)
movies_year_distributors = get_movies_per_years_per_distributors(distributors, data)
generate_data_d3("movies_per_years_per_distributor.js", "movies_per_years_per_distributor", movies_year_distributors)
genres_and_actors_number = get_count_genres_and_actors(data)
genres_number = genres_and_actors_number[0]
actors_number = genres_and_actors_number[1]
realisators_number = genres_and_actors_number[2]
production_years_number = genres_and_actors_number[3]
genres_number_formated = get_data_formated_genre_bar(genres_number, 50)
generate_data_d3("genres_bar_chart.js", "genres_number", [genres_number_formated])
actors_number_formated = get_data_formated_genre_bar(actors_number, 80)
generate_data_d3("actors_bar_chart.js", "actors_number", [actors_number_formated])
realisators_number_formated = get_data_formated_genre_bar(realisators_number, 43)
generate_data_d3("realisators_bar_chart.js", "realisators_number", [realisators_number_formated])
production_years_number_formated = get_data_formated_genre_bar(production_years_number, 700)
generate_data_d3("production_year_bar_chart.js", "production_years_number", [production_years_number_formated])
