def compare_urls(url1, url2):
    query1 = url1.split('?')[1].split('&')
    query2 = url2.split('?')[1].split('&')
    dict1 = query_to_dict(query1)
    dict2 = query_to_dict(query2)

    common = list()
    for k in dict1:
        if k in dict2:
            common.append(dict1[k])
    return common


def query_to_dict(query):
    result = {}
    for q in query:
        key, value = q.split('=')
        result[key] = value
    return result
