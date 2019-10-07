from cpanel_queries import *
from datetime import date, timedelta

# ElasticSearch URL
elasticsearch_url = "http://localhost:9200"
# cPanel index pattern name
cpanel_audit_index_pattern = 'cpanel_audit'

# Search all time frames or only the last 24 hours
search_all_time = False
if search_all_time:
    cpanel_index_pattern = "cpanel_access-*"
    whmcs_index_pattern = "apache_access-*"
else:
    yesterday = date.today() - timedelta(1)
    cpanel_index_pattern = 'cpanel_access-*-{}'.format(yesterday.strftime('%Y.%m.%d'))
    whmcs_index_pattern = 'apache_access-*-{}'.format(yesterday.strftime('%Y.%m.%d'))


cpanel_queries_list_staff = {
    'cpanel_download_phpmyadmin_dbexport': cpanel_download_phpmyadmin_dbexport,
    'cpanel_download_getsqlbackup': cpanel_download_getsqlbackup,
    'cpanel_download_getbackup_home': cpanel_download_getbackup_home,
    'cpanel_download_fullbackup': cpanel_download_fullbackup,
    'cpanel_download_filemanager': cpanel_download_filemanager,
    'cpanel_generate_fullbackup': cpanel_generate_fullbackup
}


cpanel_queries_list_customers = {
    'cpanel_download_fullbackup': cpanel_download_fullbackup,
    'cpanel_generate_fullbackup': cpanel_generate_fullbackup
}

# Mailing
path_to_results = "./tmp"
msg_subject_staff = 'cPanel Audit Report - Staff'
msg_subject_customers = 'cPanel Audit Report - Customers'
msg_from = 'Auditing Reports <reports@domain.tld>'
# List of emails to email when the staff members generates a backup
msg_to_staff = ['', '']
# List of emails to email when the customer generates a backup
msg_to_customers = ['', '']
# SMTP Server Username
smtp_username = ''
# SMTP Server Password
smtp_password = ''
# SMTP Server Hostname
smtp_hostname = ''
