# Flask/MySQL Setup

## Clone this repo

```zsh
git clone https://github.com/cmderobertis/flask_template.git
```

## Install Flask and PyMySQL

- *The Pipfiles are pre-configured, so just run the command below to install both Flask and PyMySQL.*

```zsh
pipenv install
```

---

## Modify template files accordingly

### [.gitignore](.gitignore)

- This may need to be modified depending on the frameworks or Operating System you're using.
- When in doubt, generate a new gitignore file on [Gitignore.io](https://www.toptal.com/developers/gitignore/).

### [database_name.py](database_name.py)

- Change this filename (and 'database_name' on line 19) to the name of your database.
- Have a copy of the 'ClassName' class for each table in your database. If you have 3 tables total, you'll have 3 classes total.
- Repeat the following steps for each table:
  
  1. Change 'ClassName' to your table name (in [PascalCase](https://en.wiktionary.org/wiki/Pascal_case), singular).
  2. Update the \_\_init\_\_ method to reflect the columns present in your table.
  3. Replace all instances of 'friends' with your table name.
  4. Replace all instances of 'friend' with your table name, singular.

- If everything goes well, you'll have a class for each table in your database, named after that table, with attributes corresponding to the columns present in your table. Neat!

### [mysqlconnection.py](mysqlconnection.py)

- In the 'connect' method on line 7, update the user and password to reflect your MySQL connection settings.

### [server.py](server.py)

- Line 2: Replace 'ClassName' and other classes in the import statement with the classes from your database_name.py file.
- Replace all instances of 'friends' with a table name (in [snake_case](https://en.wiktionary.org/wiki/snake_case), plural).
- Line 10: Change 'ClassName' to your table name (in [PascalCase](https://en.wiktionary.org/wiki/Pascal_case), singular).
- *Note that the code referenced in the previous two steps are meant to test the connection with the database. Feel free to modify your '/' route after running the server without error.*

---

## Test the server

Run the following:

```zsh
pipenv shell
python3 server.py
```

If the server is running without error, visit your [Localhost](http://localhost:5000) to check it out. Congratulations, you've just created a full-stack web application!
