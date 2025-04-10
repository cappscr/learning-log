# Learning Log

Learning Log is a web app that allows users to
log topics they're interested in and make journal entries as
they learn about each topic. The Learning Log home page
describes the site and invite users to either register or log in. Once
logged in, a user can create new topics, add new entries, and read
and edit existing entries.

## Project Setup

1. Create a virtual environment

```bash
python -m venv ll_env
```

2. Activate the virtual environment

```bash
source ll_env/bin/activate
```

3. Install application dependencies in the virtual environment

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

4. Running a dev server locally

```bash
python manage.py runserver
```