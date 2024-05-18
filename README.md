# Installation

First, create a file `.env` and paste the following information.
```
DB_NAME=genlms
DB_USER=root
DB_PASSWORD=root
DB_HOST=localhost
DB_PORT=3307
MS_ID=453401de-e447-4f96-a572-b99b143eb466
MS_SECRET=1Ef8Q~od4sISM~ZYv7aiQhqxsrunJQdU87Uvtdhs
```

Edit the environment as necessary. For example, if your MySQL server is running on port 3306, change it to 3306.

In real world, I should not expose the MS_SECRET in this readme file. However, this is a closed project, and we can't expect Prof to create a new Azure application just to test our assignment. So, we decided to share this secret key here.

Next, enter the following command from this directory.
```
pip install -r requirements.txt
python manage.py migrate
```

# Setting up - whitelist
## Superadmin
Please create a superadmin account via the command `python manage.py createsuperuser`. The recommended username and password for testing purposes is `admin`.
Upon creation, start the server via `python manage.py runserver`. And then visit http://localhost:8000/admin to login with your superuser credentials.
Next, under "Authentication and Authorization", add a new user, username is your student ID, password please auto generate one.
Finally, enter the first name, followed by email address. Click save.
Now, you should be able to login from http://localhost:8000/login/.

![Screenshot of the creating user steps](/static/readme-1.png)
![Screenshot of the creating user steps](/static/steps.gif)

# Running
```
python manage.py runserver
```
Upon successful, the command prompt will prompt you to visit http://localhost:8000.

## Notice
Whenever you change the DB schema, run `python manage.py migrate` to update the database schema.