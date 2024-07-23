# Aryu Book Store
This project is a test and practice small store website developed with the following technologies:
- **html, css**
- **bootstrap 5**
- **java script**
- **python, django framework**
- **django restframework**
- **redis cache database**
- **docker, git, github**

This project is purely an exercise, and the use of the mentioned technologies is only for learning, it may not be the best practice, or full of bugs, or the implementation of parts of the code may be completely unused and only for learning.

![demo aryu bookstore](https://raw.githubusercontent.com/aliaryu/aryu-bookstore/main/docs/demo.jpg?raw=true)

## Commit Conventions
This repository uses special rules for commit messages. Syntax & Example:

    <type>(<scope>): <message>
    <description>

    $ git commit -m "docs(readme): update project documention" -m "description"

Complete information: [commit conventions](https://github.com/aliaryu/aryu-bookstore/blob/main/docs/commit-conventions.md)

## Entity Relationship Model
![entity relationship model](https://github.com/aliaryu/aryu-bookstore/blob/main/docs/entity-relationship-diagram.png?raw=true)

## How To Use
First, clone the project:

    git clone https://github.com/aliaryu/aryu-bookstore.git

If you don't want to use docker, then **DEBUG** must be **True** (according to the .env file) and after creating the virtual environment, execute the following commands in order:

    pip install -r requirements.txt
    python manage.py makemigrations
    python manage.py migrate
    python scripts/fill_database/filldb.py
    python manage.py runserver

The **filldb.py** fills your database with predefined data so that there is data when testing the project.

If you want to use docker, according to the **DEBUG** status, you can run the following command:

    docker-compose up -d --build

## Contact
Email: <a href="mailto:aliaryu@yahoo.com">aliaryu@yahoo.com</a>
