import re


# Проверка на возможность преобразования в float число
def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


# Преобразование строки в целый, вещественный или строковый формат данных
def handler_deli(value):
    if (value[1]).isdigit():
        return int(value[1])
    elif isfloat(value[1]):
        return float(value[1])
    else:
        to_str = re.findall(r'[^\" ()]\w*', value[1])
        return to_str[0]


def parse(query):
    dict_query = {}
    handler_query = re.findall(r'\w*[>!=<]\S*[^() ]', query)
    query_split = query.split(' ')
    if ('AND' or "OR") in query_split:
        for i, j in enumerate(query_split):
            if (j == 'AND' or j == 'OR') and not (query_split[i - 1]).startswith('(') and not (
                    query_split[i + 1]).endswith(')'):
                deli_left = re.findall(r'[>!=<]', query_split[i - 1])
                deli_right = re.findall(r'[>!=<]', query_split[i + 1])
                dict_query['type'], dict_query['op'] = 'node', j
                if not (query_split[i - 1]).startswith('(') and not (query_split[i - 1]).endswith(')'):
                    ids = query_split[i - 1].split(deli_left[0])[0]
                    literal = query_split[i - 1].split(deli_left[0])
                    dict_query.update(
                        {'left': {'type': 'leaf', 'op': deli_left[0], 'id': ids,
                                  'literal': handler_deli(literal)}})
                if not (query_split[i + 1]).startswith('(') and not (query_split[i + 1]).endswith(')'):
                    ids = query_split[i + 1].split(deli_right[0])[0]
                    literal = query_split[i + 1].split(deli_right[0])
                    dict_query.update(
                        {'right': {'type': 'leaf', 'op': deli_right[0], 'id': ids,
                                   'literal': handler_deli(literal)}})
                if (query_split[i - 3]).startswith('(') and (query_split[i - 1]).endswith(')'):
                    handler_query_left = re.findall(r'\w*[>!=<]\S*[^() ]', query_split[i - 3])
                    handler_query_right = re.findall(r'\w*[>!=<]\S*[^() ]', query_split[i - 1])
                    deli_left = re.findall(r'[>!=<]', query_split[i - 3])
                    deli_right = re.findall(r'[>!=<]', query_split[i - 1])
                    ids_l = handler_query_left[0].split(deli_left[0])[0]
                    ids_r = handler_query_right[0].split(deli_right[0])[0]
                    literal_left = handler_query_left[0].split(deli_left[0])
                    literal_right = handler_query_right[0].split(deli_right[0])
                    dict_query.update(
                        {'left': {'type': 'node', 'op': query_split[i - 2], 'left': {
                            'type': 'leaf', 'op': deli_left[0], 'id': ids_l, 'literal': handler_deli(literal_left)
                        }, 'right': {'type': 'leaf', 'op': deli_right[0], 'id': ids_r,
                                     'literal': handler_deli(literal_right)}}})

                if (query_split[i + 1]).startswith('(') and (query_split[i + 3]).endswith(')'):
                    handler_query_left = re.findall(r'\w*[>!=<]\S*[^() ]', query_split[i + 1])
                    handler_query_right = re.findall(r'\w*[>!=<]\S*[^() ]', query_split[i + 3])
                    deli_left = re.findall(r'[>!=<]', query_split[i + 1])
                    deli_right = re.findall(r'[>!=<]', query_split[i + 3])
                    ids_l = handler_query_left[0].split(deli_left[0])[0]
                    ids_r = handler_query_right[0].split(deli_right[0])[0]
                    literal_left = handler_query_left[0].split(deli_left[0])
                    literal_right = handler_query_right[0].split(deli_right[0])
                    dict_query.update(
                        {'right': {'type': 'node', 'op': query_split[i + 2], 'left': {
                            'type': 'leaf', 'op': deli_left[0], 'id': ids_l, 'literal': handler_deli(literal_left)
                        }, 'right': {'type': 'leaf', 'op': deli_right[0], 'id': ids_r,
                                     'literal': handler_deli(literal_right)}}})
    else:
        deli = re.findall(r'[>!=<]', query)[0]
        dict_query['type'] = 'leaf'
        dict_query['op'] = deli
        dict_query['id'] = query.split(deli)[0]
        if (query.split(deli)[1]).isdigit():
            dict_query['literal'] = int((query.split(deli)[1]))
        elif isfloat((query.split(deli)[1])):
            dict_query['literal'] = float((query.split(deli)[1]))
        else:
            to_str = re.findall(r'[^\" ()]\w*', query)
            dict_query['literal'] = to_str[2]

    return dict_query
