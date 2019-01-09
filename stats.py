from collections import Counter

import _vk


def normalize_geo(dict_list):
    overall = sum([x['mp_city'][2] for x in dict_list])
    for i in range(len(dict_list)):
        dict_list[i]['mp_city'][1] = dict_list[i]['mp_city'][1] * (dict_list[i]['mp_city'][2]/overall)
        dict_list[i]['mp_country'][1] = dict_list[i]['mp_country'][1] * (dict_list[i]['mp_country'][2] / overall)

    probabilities_city = {}
    probabilities_country = {}
    for d in dict_list:
        if d['mp_city'][0] not in probabilities_city.keys():
            probabilities_city[d['mp_city'][0]] = d['mp_city'][1]
        else:
            probabilities_city[d['mp_city'][0]] += d['mp_city'][1]
        if d['mp_country'][0] not in probabilities_country.keys():
            probabilities_country[d['mp_country'][0]] = d['mp_country'][1]
        else:
            probabilities_country[d['mp_country'][0]] += d['mp_country'][1]

    return probabilities_city, probabilities_country


def find_similar(ids, session):

    # if dates are controversial then omit all provided info
    # not necessary for now
    def is_controversial(obj):
        return False

    def get_age(objects):
        return 0

    def get_geo(objects):
        def count_with_nones(list_of_names, counter):
            nones = list_of_names.count(None)
            wo_none = [x for x in list_of_names if x is not None]
            temp_counter = Counter(wo_none)
            try:
                k = nones / sum(temp_counter.values())
            except ZeroDivisionError:
                print(1)
            for name in temp_counter:
                counter.update({name: (k * temp_counter[name] + temp_counter[name]) / len(list_of_names)})

            return counter
        # sort ids out first
        city_counter = Counter()
        country_counter = Counter()
        for obj in objects:
            cities = [obj["city_id"]] + obj["schools_city"] + obj["universities_city"] + obj["career_city_id"] \
                     + obj["schools_city"]
            if cities.count(None) == len(cities):
                city_counter.update({None: 1})
            else:
                city_counter = count_with_nones(cities, city_counter)

            countries = [obj["country_id"]] + obj["schools_country"] + obj["universities_country"] \
                        + obj["career_country_id"] + obj["schools_country"]
            if countries.count(None) == len(countries):
                country_counter.update({None: 1})
            else:
                country_counter = count_with_nones(countries, country_counter)

        most_common_city = city_counter.most_common()[0]
        most_common_country = country_counter.most_common()[0]

        result = {"mp_city": [most_common_city[0], most_common_city[1] / sum(city_counter.values()), len(objects)],
                  "mp_country": [most_common_country[0], most_common_country[1] / sum(country_counter.values()), len(objects)]}
        return result

    def get_schools(objects):
        return 0

    def get_uni(objects):
        return 0
    def get_career(objects):
        return 0

    def get_langs(objects):
        return 0

    def get_politics(objects):
        return 0

    def get_religion(objects):
        return 0

    def get_all_data(objects):
        potential_age = get_age(objects)
        potential_geo = get_geo(objects)
        potential_school = get_schools(objects)
        potential_uni = get_uni(objects)
        potential_langs = get_langs(objects)
        potential_politics = get_politics(objects)
        potential_religion = get_religion(objects)

    fields_to_copy = ["bdate", ["city", ["id", "title"]], ["country", ["id"]],
                      "home_town", ["universities", ["country", "city",
                                                     "id", "faculty", "chair", "graduation"]],
                      ["schools", ["id", "country", "city"]], ["personal", ["langs", "political", "religion"]],
                      ["career", ["city_id", "company", "group_id", "country_id"]],
                      ["military", ["unit_id", "country_id", "from", "until"]]]

    # create objs with data to work with
    def create_data_objs(i_data, ftc):
        user_list = []
        fields_to_copy_i = ftc

        for user in i_data:
            obj = {}
            # empty fields interfere
            for key in fields_to_copy_i:
                try:
                    if isinstance(key, list):
                        if not user[key[0]]:
                            del user[key[0]]
                    else:
                        if not user[key]:
                            del user[key]
                except KeyError:
                    continue

            # adding all info in dict, unifying info, appending resulting dict to user_list
            for key in fields_to_copy_i:
                if isinstance(key, list):
                    if key[0] in ("schools", "universities", "career", "military"):
                        try:
                            user[key[0]]
                        except KeyError:
                            for field in key[1]:
                                obj.update({"_".join((key[0], field)): [None]})
                        else:
                            for field in key[1]:
                                obj.update({"_".join((key[0], field)): []})
                            for frame in user[key[0]]:
                                for field in key[1]:
                                    try:
                                        obj["_".join((key[0], field))].append(frame[field])
                                    except KeyError:
                                        obj["_".join((key[0], field))].append(None)
                    else:
                        try:
                            user[key[0]]
                        except KeyError:
                            for field in key[1]:
                                obj.update({"_".join((key[0], field)): None})
                        else:
                            for field in key[1]:
                                try:
                                    obj.update({"_".join((key[0], field)): user[key[0]][field]})
                                except KeyError:
                                    obj.update({"_".join((key[0], field)): None})
                else:
                    try:
                        obj.update({key: user[key]})
                    except KeyError:
                        obj.update({key: None})

            user_list.append(obj)

        return user_list

    data = _vk.get_all_info(session=session, targets=",".join(ids))
    objs = create_data_objs(data, fields_to_copy)

    c = {}
    for key_o in fields_to_copy:
        c.update({key_o[0]: 1})

    return get_geo(objs)
