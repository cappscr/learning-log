#!/bin/bash
python3 manage.py collectstatic && gunicorn --workers 2 ll_project.wsgi