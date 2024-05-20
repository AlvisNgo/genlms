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
```
# Setting up
## Create Database
Using command prompt or any GUI application, please create a new database with `genlms` as it name. Make sure you can login to the database.
After that, please run `python manage.py migrate` to create all the necessary tables.
## Loading of dummy data
We will need to load dummy data into the database. Please use those command line by line.
```
python manage.py loaddata user
python manage.py loaddata lmsadmin
python manage.py loaddata course
python manage.py loaddata courseadmin
```

Now, you'll be able to login to the system with your SIT and Glasgow account. For testing purposes, the SIT is a student account. The Glasgow is the LMS admin account.
## Add course to your student account
Upon logging in, you'll notice that you're not in any course. To add course to your student account, please refer to [Add course to student](#add-course-to-student)
# Running
```
python manage.py runserver
```
Upon successful, the command prompt will prompt you to visit http://localhost:8000.
# Notice
Whenever you change the DB schema, run `python manage.py migrate` to update the database schema.

# Admin Panel
Visit http://localhost:8000/admin to login with your superuser credentials - default: `admin` for both password and username.

## Add user to white list
Next, under "Authentication and Authorization", add a new user, username is your student ID, password please auto generate one.

Finally, enter the first name, followed by email address. Click save.

Now, you should be able to login from http://localhost:8000/login/.

![Screenshot of the creating user steps](/static/steps.gif)

## Add course to student
In the admin panel, under ["LMS" -> "Enrolled Course"](http://localhost:8000/admin/lms/enrolledcourse/), you may assigned yourself a course.
Now, you may refresh the dashboard and it should appear under "My Course" section.

## Misc
In the admin panel, you can create new course, add/remove user as LMS admin, add admin as course administrator.
