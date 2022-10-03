# Web Scraper

## The tool scrapes public repositories of the github user entered by the client, stores into a database and shows the list of repositories scraped.

The backend is written in Python and the frontend is written in Javascript using React framework
The following technologies are used:

1. Database: sqlite3
2. Web Server: Flask
3. Libraries for scraping: requests, BeautifulSoup4

## Backend

Two tables are constructed to store information:

1. github_user - stores an ID (primary key) and user name
2. github_repository - store an ID (primary key), user ID (foreign key), repository name

The Flask app is run with the following functions:

1. Route 1: /users: Returns a list of all the users present in the database
   Response = {
   user_list: [{"user_name":"name1"}, {"user_name":"name2"}]
   }
2. Route 2: /users/<user_name>: Scrapes the public repositories of the user.
   It does the following checks:
   1. Checks if the user name exists in the database
      If true: Response = {
      message: "User exists in DB",
      status: "USER_EXISTS"
      }
   2. Checks if the user name exists in github
      If true: Response = {
      message: "User does not exist",
      status: "USER_NOT_FOUND"
      }
      If the above two checks fail, the public repositories are scraped and stored to the databse with the following response
      Response = {
      message: "User has been successfully added to database",
      status: "USER_ADDED"
      }
3. Route 3: /users/<user_name>/repositories: Shows the list of repository names for a given user name. At a time only 10 repository names are shown, if there are more, they are shown in the following pages.
   Response = {
   user_name: user_name,
   repository: repository_list,
   total: total_repositories
   }

## Frontend

Main URL: http://localhost:3000/users

On page load, the application calls Route 1 mentioned in the backend section to load the list of user names present in the database.

The dropdown menu consists of the list of all the user names present in the database. On selection of the user name from the dropdown, the public repositories for the same will be displayed by calling Route 3 mentioned in the backend section. A set of 10 repositories are displayed per page.

1. If number of repositories are less than or equal to 10: the previous and next buttons will be disabled
2. If there are more than 10 repositories:

- On the first page: only the next button will be enabled
- On the last page: only the previous button will be enabled
- On the remaining pages: both next and previous buttons will be enabled
  On selection of user name from the dropdown menu, URL: http://localhost:3000/users/<user_name>/repositories
  A query parameter named "page" is used to keep track of the page number

On click of the submit button after entering a user name in the input box, Route 2 mentioned in the backend section is called to verify if the user already exists in the database, or if the user name does not exist in github or if the user has been added. The message response is displayed for the client to see. After the new user has been added, it is redirected to URL "http://localhost:3000/users/<user_name>/repositories" showing the list of repositories present for the said user in the database.

## To execute:

1. Build docker compose file: docker-compose build
2. Run the docker compose file: docker-compose up
3. Open: http://localhost:3000/users
