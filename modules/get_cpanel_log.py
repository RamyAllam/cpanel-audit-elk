import requests


def do_get_cpanel_log(elasticsearch_url, index_pattern, cpanel_query):
    request_url = "{}/{}/_search?pretty&size=1000".format(elasticsearch_url, index_pattern)
    headers = {'Content-Type': 'application/json'}

    request = requests.get(request_url, headers=headers, json=cpanel_query).json()
    request = request['hits']['hits']
    return request
