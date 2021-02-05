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


# Разгрузочная функция для отлавливания id и literal
def calculate_data(left, right, ld, rd):
    ids_l = left[0].split(ld[0])[0]
    literal_left = left[0].split(ld[0])
    ids_r = right[0].split(rd[0])[0]
    literal_right = right[0].split(rd[0])
    context = (ids_l, literal_left, ids_r, literal_right)
    return context


def parse(query):
    dict_query = {}
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
                    content_l = calculate_data(handler_query_left, handler_query_right, deli_left, deli_right)
                    dict_query.update(
                        {'left': {'type': 'node', 'op': query_split[i - 2], 'left': {
                            'type': 'leaf', 'op': deli_left[0], 'id': content_l[0],
                            'literal': handler_deli(content_l[1])
                        }, 'right': {'type': 'leaf', 'op': deli_right[0], 'id': content_l[2],
                                     'literal': handler_deli(content_l[3])}}})
                if (query_split[i + 1]).startswith('(') and (query_split[i + 3]).endswith(')'):
                    handler_query_left = re.findall(r'\w*[>!=<]\S*[^() ]', query_split[i + 1])
                    handler_query_right = re.findall(r'\w*[>!=<]\S*[^() ]', query_split[i + 3])
                    deli_left = re.findall(r'[>!=<]', query_split[i + 1])
                    deli_right = re.findall(r'[>!=<]', query_split[i + 3])
                    content_r = calculate_data(handler_query_left, handler_query_right, deli_left, deli_right)
                    dict_query.update(
                        {'right': {'type': 'node', 'op': query_split[i + 2], 'left': {
                            'type': 'leaf', 'op': deli_left[0], 'id': content_r[0],
                            'literal': handler_deli(content_r[1])
                        }, 'right': {'type': 'leaf', 'op': deli_right[0], 'id': content_r[2],
                                     'literal': handler_deli(content_r[3])}}})
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

