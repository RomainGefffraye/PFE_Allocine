class Movies_per_distributor_per_year:
    def __init__(self, data, distributor):
        self.distributor = distributor
        movies_per_year = {}
        for attribute, value in data.iteritems():
            if value["distributor"] == distributor:
                if value["production_year"] in movies_per_year:
                    movies_per_year[value["production_year"]] += 1
                else:
                    movies_per_year[value["production_year"]] = 1
        data_js = []
        for key, value in movies_per_year.iteritems():
            if key != None and key != "":
                data_format = {}
                data_format["y"] = int(value)
                data_format["x"] = int(key)
                data_js.append(data_format)
        if len(data_js) > 20:
            self.relevant = True
        else:
            self.relevant = False
        self.movies_per_year = movies_per_year
        self.data_for_d3 = sorted(data_js, key=lambda k: k['x'])
