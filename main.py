from crypt import methods
from email import message
import imp
from shutil import unregister_unpack_format
from unicodedata import name
from unittest import result
from urllib import response
import requests
from bs4 import BeautifulSoup
import sqlite3
from sqlite3 import Error
from flask import Flask, jsonify, redirect, render_template, request, url_for
import time

app = Flask(__name__)


def create_connection():
    conn = None
    try:
        conn = sqlite3.connect("github_db.db", check_same_thread=False)
        conn.execute("PRAGMA foreign_keys = 1")
    except Error as e:
        print(e)
    return conn


def store_to_github_user(table_name, user_name):
    conn = create_connection()
    cur = conn.cursor()
    sql_statement = f"""
    INSERT INTO {table_name} (user_name) VALUES ('{user_name}');
    """
    cur.execute(sql_statement)
    conn.commit()
    conn.close()


def store_to_github_repo(table_name, repo_name, user_id):
    conn = create_connection()
    cur = conn.cursor()
    sql_statement = f"""
        INSERT INTO {table_name} (user_id, repo_name) VALUES ({user_id}, '{repo_name}');
        """
    cur.execute(sql_statement)
    conn.commit()
    conn.close()


def retrieve_from_database(user_name, page_number):
    conn = create_connection()
    cur = conn.cursor()
    number_of_repositories = 0
    if page_number > 1:
        number_of_repositories = (page_number-1)*10
    cur.execute(f"""
        SELECT repo_name FROM github_repository, github_user 
        WHERE github_user.user_name='{user_name}' AND github_user.id=github_repository.user_id 
        ORDER BY github_repository.id LIMIT 10 OFFSET {number_of_repositories};
    """)
    repository_list = cur.fetchall()
    result_repository_list = []
    for repository in repository_list:
        result_repository_list.append({"name": repository[0]})
    conn.close()
    return result_repository_list


def check_user_name(user_name):
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(f"""SELECT count(*) FROM github_user
    WHERE user_name='{user_name}';
    """)
    count = cur.fetchall()
    conn.close()
    return count[0][0]


def scrape_user_repositories(user_name):
    next_page = True
    page_number = 1
    repositories = []
    while next_page:
        url = f'https://github.com/{user_name}?page={page_number}&tab=repositories'
        page = requests.get(url)
        if page.status_code == 404:
            return page.status_code
        page_content = BeautifulSoup(page.content, 'html.parser')
        repo_names = page_content.find_all(
            'a', attrs={"itemprop": "name codeRepository"})
        for _, i in enumerate(repo_names):
            repositories.append({"name": i.text.strip().split("\n")[0]})
        if page_content.find('a', class_="next_page"):
            page_number += 1
        else:
            next_page = False

    return {"repositories": repositories}


@app.route("/users", methods=['GET'])
def return_users_list():
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("""SELECT user_name FROM github_user;""")
    user_name_list = cur.fetchall()
    conn.close()
    result_user_name = []
    for user_name in user_name_list:
        result_user_name.append({"user_name": user_name[0]})
    response = jsonify(user_list=result_user_name)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/users/<user_name>", methods=['GET'])
def scrape_user_info(user_name):
    # check if user name exists in database
    check_for_username = check_user_name(user_name)
    if check_for_username != 0:
        response = jsonify(message="User exists in DB", status="USER_EXISTS")
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response
    else:
        # if user does not exist scrape data
        github_info = scrape_user_repositories(user_name)
        # check for error code
        if github_info == 404:
            response = jsonify(message="User does not exist",
                               status="USER_NOT_FOUND")
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response
        else:
            # if no error store repositories to a list
            repository_list = github_info['repositories']
            store_to_github_user("github_user", user_name)
            # return the user id
            conn = create_connection()
            cur = conn.cursor()
            cur.execute(
                f"""SELECT id FROM github_user WHERE user_name = '{user_name}';""")
            id = cur.fetchall()
            conn.close()
            # using user id store repository name
            for repo in repository_list:
                store_to_github_repo("github_repository",
                                     repo['name'], id[0][0])
            response = jsonify(
                message="User has been successfully added to database", status="USER_ADDED")
            response.headers.add("Access-Control-Allow-Origin", "*")
            return response


@app.route("/users/<user_name>/repositories", methods=['GET'])
def return_user_repo(user_name):
    args = request.args
    page_number = args.get("page")
    if page_number is None:
        page_number = 1
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(
        f"SELECT COUNT(*) FROM github_repository, github_user WHERE github_user.user_name ='{user_name}' AND github_user.id=github_repository.user_id;")
    total_repositories = cur.fetchall()
    conn.close()
    repository_list = retrieve_from_database(user_name, int(page_number))
    response = jsonify(
        user_name=user_name, repository=repository_list, total=total_repositories[0][0])
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


if __name__ == "__main__":
    conn = create_connection()
    cur = conn.cursor()
    # create tables github_user and github_repositories if it does not exist
    cur.execute("""
    CREATE TABLE IF NOT EXISTS [github_user] (
        [id] INTEGER PRIMARY KEY AUTOINCREMENT,
        [user_name] TEXT
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS [github_repository] (
        [id] INTEGER PRIMARY KEY AUTOINCREMENT,
        [user_id] INTEGER NOT NULL,
        [repo_name] TEXT,
        FOREIGN KEY (user_id) REFERENCES github_user (id)
    );
    """)
    conn.commit()
    conn.close()

    app.run()
