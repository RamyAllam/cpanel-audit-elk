import requests
from config import *
from modules import get_cpanel_log, get_whmcs_log, cpanel_query_title, send_mail
import os
import random
import string
import datetime


def start():

    audit_data_found = False
    process_id = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(10))
    results_filename = "{}/{}.txt".format(path_to_results, process_id)
    if not os.path.exists(path_to_results):
        os.makedirs(path_to_results)

    time_now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    try:
        with open("{}".format(results_filename), 'a') as file:
            file.write("# cPanel audit for shared hosting - {}\n\n".format(time_now))
    except Exception as e:
        return "Exception: {}".format(e)

    # Loop through cPanel queries
    for query_name, query_value in cpanel_queries_list_staff.items():

        # Query cPanel logs
        cpanel_results = get_cpanel_log.do_get_cpanel_log(elasticsearch_url, cpanel_index_pattern, query_value)

        # Extract data from cPanel results
        for i in cpanel_results:
            cpanel_clientip = i['_source']['clientip']
            cpanel_request = i['_source']['request']
            cpanel_username = i['_source']['username']
            cpanel_access_time = i['_source']['timestamp']
            cpanel_host = i['_source']['host']
            cpanel_browser = i['_source']['name']
            cpanel_os = i['_source']['os']
            cpanel_country = i['_source']['geoip']['country_name']
            cpanel_request_type = cpanel_query_title.do_cpanel_query_title(query_name)

            # Get results from WHMCS against the cPanel data
            whmcs_results = get_whmcs_log.do_get_whmcs_log(elasticsearch_url, whmcs_index_pattern, cpanel_clientip)
            whmcs_username = None
            # Extract data from WHMCS results
            if whmcs_results:
                for z in whmcs_results:
                    whmcs_username = z['_source']['auth']
                    # Break on first match
                    if whmcs_username:
                        break

                # Double check that cPanel username field in cPanel elasticsearch documents does not equal dash
                if whmcs_username != "-":
                    try:
                        with open("{}".format(results_filename), 'a') as file:
                            file.write("IP: {}\n".format(cpanel_clientip))
                            file.write("Request: {}\n".format(cpanel_request))
                            file.write("Request Type: {}\n".format(cpanel_request_type))
                            file.write("cPanel Username: {}\n".format(cpanel_username))
                            file.write("Hostname: {}\n".format(cpanel_host))
                            file.write("Staff Username: {}\n".format(whmcs_username))
                            file.write("Staff Browser: {}\n".format(cpanel_browser))
                            file.write("Staff OS: {}\n".format(cpanel_os))
                            file.write("Staff Country: {}\n".format(cpanel_country))
                            file.write("Staff Access-time: {}\n".format(cpanel_access_time))
                            file.write("==========================================\n")
                            file.close()
                    except Exception as e:
                        return "Exception: {}".format(e)

                    request_url = "{}/{}/_doc/?pretty".format(elasticsearch_url, cpanel_audit_index_pattern)
                    headers = {'Content-Type': 'application/json'}
                    cpanel_audit_json = {
                        'clientip': cpanel_clientip,
                        'username': cpanel_username,
                        'request': cpanel_request,
                        'request_type': cpanel_request_type,
                        'host': cpanel_host,
                        'staff_username': whmcs_username,
                        'staff_browser': cpanel_browser,
                        'staff_os': cpanel_os,
                        'staff_country': cpanel_country,
                        '@timestamp': cpanel_access_time,
                    }
                    requests.post(request_url, headers=headers, json=cpanel_audit_json)
                    audit_data_found = True
                    # results_documents_list.append(save_to_elasticsearch.json()['_id'])
    if audit_data_found:
        send_mail_results = send_mail.do_send_mail(results_filename=results_filename, msg_subject=msg_subject_staff,
                                                   msg_to=msg_to_staff)
        if send_mail_results:
            print("Send mail success")
            # os.remove(results_filename)
        else:
            print("Send mail failed")


start()
