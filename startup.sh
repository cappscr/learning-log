#!/bin/bash
python3 manage.py migrate && gunicorn --workers 2 ll_project.wsgi