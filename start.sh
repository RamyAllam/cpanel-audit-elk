#!/bin/bash
cd /home/$USER/cpanel-audit-elk
source venv/bin/activate
venv/bin/python3 audit_customers_logs.py
sleep 5
venv/bin/python3 audit_staff_logs.py