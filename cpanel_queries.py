cpanel_download_phpmyadmin_dbexport = {
    "query": {
        "bool": {
            "must": [
                {"match": {"request": "phpMyAdmin"}},
                {"exists": {"field": "username"}},
                {"bool": {
                    "should": [
                        {"term": {"extra_fields": "2082"}},
                        {"term": {"extra_fields": "2083"}}
                    ]
                }},

            ],
            "filter": [
                {"match": {"verb": "POST"}},
                {"term": {"request": "export.php"}},
            ]
        },
    }
}

cpanel_download_getsqlbackup = {
    "query": {
        "bool": {
            "must": [
                {"match": {"request": "getsqlbackup"}},
                {"exists": {"field": "username"}},
                {"bool": {
                    "should": [
                        {"term": {"extra_fields": "2082"}},
                        {"term": {"extra_fields": "2083"}}
                    ]
                }},

            ],
            "filter": [
                {"match": {"verb": "GET"}},
            ]
        },
    }
}

cpanel_download_getbackup_home = {
    "query": {
        "bool": {
            "must": [
                {"match": {"request": "getbackup"}},
                {"exists": {"field": "username"}},
                {"bool": {
                    "should": [
                        {"term": {"extra_fields": "2082"}},
                        {"term": {"extra_fields": "2083"}}
                    ]
                }},
            ],
            "filter": [
                {"match": {"verb": "GET"}},
            ]
        },
    }
}

cpanel_download_fullbackup = {
    "query": {
        "bool": {
            "must": [
                {"match": {"request": "download?file="}},
                {"exists": {"field": "username"}},
                {"bool": {
                    "should": [
                        {"term": {"extra_fields": "2082"}},
                        {"term": {"extra_fields": "2083"}}
                    ]
                }},
            ],
            "filter": [
                {"match": {"verb": "GET"}},
                {"term": {"referrer": "fullbackup.html"}},
            ]
        },
    }
}

cpanel_download_filemanager = {
    "query": {
        "bool": {
            "must": [
                {"term": {"request": "download"}},
                {"exists": {"field": "username"}},
                {"match": {"verb": "GET"}},
                {"term": {"referrer": "filemanager"}},
                {"bool": {
                  "should": [
                      {"term": {"extra_fields": "2082"}},
                      {"term": {"extra_fields": "2083"}}
                  ]
                }},
            ],
        },
    }
}

# No download here, it only generates
cpanel_generate_fullbackup = {
    "query": {
        "bool": {
            "must": [
                {"term": {"request": "dofullbackup.html"}},
                {"exists": {"field": "username"}},
                {"match": {"verb": "POST"}},
                {"term": {"referrer": "fullbackup.html"}},
                {"bool": {
                  "should": [
                      {"term": {"extra_fields": "2082"}},
                      {"term": {"extra_fields": "2083"}}
                  ]
                }},
            ],
        },
    }
}
