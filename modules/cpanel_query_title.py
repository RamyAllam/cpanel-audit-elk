def do_cpanel_query_title(query):
    query_explanation = ''
    if query == "cpanel_download_phpmyadmin_dbexport":
        query_explanation = "cPanel phpMyAdmin export database"

    elif query == "cpanel_download_getsqlbackup":
        query_explanation = "cPanel download database from internal backup"

    elif query == "cpanel_download_getbackup_home":
        query_explanation = "cPanel download home-directory from internal backup"

    elif query == "cpanel_download_fullbackup":
        query_explanation = "cPanel download full account backup from internal backup"

    elif query == "cpanel_download_filemanager":
        query_explanation = "cPanel download a file from FileManager"

    elif query == "cpanel_generate_fullbackup":
        query_explanation = "cPanel generate full backup. (Not necessarily downloaded)"

    return query_explanation
