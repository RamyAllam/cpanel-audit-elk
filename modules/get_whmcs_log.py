import requests


def do_get_whmcs_log(elasticsearch_url, index_pattern, clientip):
    request_url = "{}/{}/_search?pretty&size=1000".format(elasticsearch_url, index_pattern)
    headers = {'Content-Type': 'application/json'}
    whmcs_search_ip = {
        "query": {
            "bool": {
                "must": [
                    {"match": {"request": "/admin/"}},
                    {"exists": {"field": "auth"}},
                    {"match": {"clientip": clientip}},
                ],
                "must_not": [
                    {"match": {"auth": "-"}},
                ],
            },
        }
    }
    request = requests.get(request_url, headers=headers, json=whmcs_search_ip).json()
    request = request['hits']['hits']
    return request
