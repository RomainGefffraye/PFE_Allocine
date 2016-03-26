from python_class_function.all_function import *

#create_all_movies_file()

with open('data/all_movies.json') as data_file:
    data = json.load(data_file)

print data["Terre lointaine"]
#with open('d3_visualisation/data/sunburst.json', 'w') as fp:
#    json.dump(getMoviesPerProductor(data), fp)

#distributors = get_set_of_distributors(data)
#data_to_save = get_movies_per_years_per_distributors(distributors, data)
#generate_data_d3("movies_per_years_per_distributor.js", data_to_save)
