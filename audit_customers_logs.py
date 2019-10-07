from config import *
from modules import get_cpanel_log, get_whmcs_log, cpanel_query_title, send_mail
import os
import random
import string
import datetime


def start():

    audit_data_found_customers = False

    process_id = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(10))
    results_filename = "{}/{}.txt".format(path_to_results, process_id)
    if not os.path.exists(path_to_results):
        os.makedirs(path_to_results)

    time_now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    try:
        with open("{}".format(results_filename), 'a') as file:
            file.write("# cPanel audit for cPanel hosting - {}\n\n".format(time_now))
    except Exception as e:
        return "Exception: {}".format(e)

    # Loop through cPanel queries
    for query_name, query_value in cpanel_queries_list_customers.items():

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

            # Set whmcs_username as None by default
            whmcs_username = None

            # Extract data from WHMCS results
            if whmcs_results:
                for z in whmcs_results:
                    whmcs_username = z['_source']['auth']
                    # Break on first match
                    if whmcs_username:
                        break

            # If no WHMCS username found, still None or has dash value
            elif whmcs_username == "-" or not whmcs_username:
                # Export the results to file
                try:
                    with open("{}".format(results_filename), 'a') as file:
                        file.write("IP: {}\n".format(cpanel_clientip))
                        file.write("Request: {}\n".format(cpanel_request))
                        file.write("Request Type: {}\n".format(cpanel_request_type))
                        file.write("cPanel Username: {}\n".format(cpanel_username))
                        file.write("Hostname: {}\n".format(cpanel_host))
                        file.write("Customer Browser: {}\n".format(cpanel_browser))
                        file.write("Customer OS: {}\n".format(cpanel_os))
                        file.write("Customer Country: {}\n".format(cpanel_country))
                        file.write("Customer Access-time: {}\n".format(cpanel_access_time))
                        file.write("==========================================\n")
                        file.close()
                except Exception as e:
                    return "Exception: {}".format(e)

                audit_data_found_customers = True

    if audit_data_found_customers:
        send_mail_results = send_mail.do_send_mail(results_filename=results_filename, msg_subject=msg_subject_customers,
                                                   msg_to=msg_to_customers)
        if send_mail_results:
            print("Send mail success")
            # os.remove(results_filename)
        else:
            print("Send mail failed")


start()
