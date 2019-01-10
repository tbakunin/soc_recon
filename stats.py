from collections import Counter
import _vk


# data in a form of [(id, prob, card), ...]
def normalize_data(list_list):
    overall = sum([x[2] for x in list_list])
    for i in range(len(list_list)):
        list_list[i][1] = list_list[i][1] * (list_list[i][2]/overall)
        list_list[i][1] = list_list[i][1] * (list_list[i][2] / overall)

    probabilities = {}
    for d in list_list:
        if d[0] not in probabilities.keys():
            probabilities[d[0]] = d[1]
        else:
            probabilities[d[0]] += d[1]

    return probabilities


def calc_prob(sims):
    print(sims)
    overall = sum(x[1] for x in sims)
    cardinality = {}
    for d in sims:
        if d[0] not in cardinality.keys():
            cardinality[d[0]] = d[1]
        else:
            cardinality[d[0]] += d[1]

    for key in cardinality.keys():
        cardinality[key] = cardinality[key] / overall

    return list(cardinality.items())


def find_similar(ids, session, datatype):

    # if dates are controversial then omit all provided info
    # not necessary for now
    def is_controversial(obj):
        return False

    def get_age(objects):
        return 0

    def get_data(objects, dtype):
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

        if dtype == "city":
            fields = ["city_id", "schools_city", "universities_city", "career_city_id"]
        elif dtype == "country":
            fields = ["country_id", "schools_country", "universities_country", "career_country_id"]
        elif dtype == "school":
            fields = ["schools_id"]
        elif dtype == "university":
            fields = ["universities_id"]
        else:
            raise Exception("Wrong data type")

        counter = Counter()
        for obj in objects:
            entities = [obj[x] for x in fields]
            entities = [x[0] if isinstance(x, list) else x for x in entities]
            if entities.count(None) == len(entities):
                counter.update({None: 1})
            else:
                counter = count_with_nones(entities, counter)

        most_common = counter.most_common()[0][0]
        # result = [most_common[0], most_common[1] / sum(counter.values()), len(objects)]
        return most_common, len(objects)

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

    return get_data(objs, datatype)
