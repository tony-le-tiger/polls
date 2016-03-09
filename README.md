# usma-it394-polls
This is a version of the official Django tutorial application configured for deployment into a production environment on Heroku.


# Getting started
Start your DAD virtual environment.
```
& $Env:WORKON_HOME\DAD\Scripts\activate.ps1
```
Change to your project directory
```
cd $Env:PROJECT_HOME\DAD
```
Then clone this repository.  
```
git clone git@github.com:usma-it394/umsa-it394-polls.git
```

Change your current working directory to the clone'd project directory.
```
cd usma-it394-polls
```
Install the packages from requirements.txt (you probably already have these installed in your DAD environment):
```
pip install -r requirements.txt
```

Then set the DATABASE_URL environment variable. Finally, create the initial local database structure and interactively create the initial local security principal with:
```
python manage.py syncdb
```

You can view the polls app running locally by starting the project with
```
python manage.py runserver
```
# Deployment
The in-class exercise from lesson 04 covers steps how to deploy into the production environment on Heroku.

## Deploy into production
After you have cloned this repository you can deploy it to heroku.  First you'll need to login to your heroku account with:
```
heroku login
```
Then tell heroku to create a new application with:
```
heroku create
```
The "heroku create" command will add a new remote to your local git repo.  You can see it with:
```
git remote -v
```
Now you can push the local repo to heroku.  This is how you "deploy your project into the production environment on Heroku".
```
git push heroku master
```
You can observe the status of the application on heroku with
```
heroku logs
heroku ps
```

## Remote data management commands
We are separated from Heroku by a firewall that blocks interactive access to Heroku one-off dynos (See: https://devcenter.heroku.com/articles/one-off-dynos).  Because of this you'll need to interact with Heroku using the run:detached option.

To destructively reset Heroku PostgreSQL database
```
heroku pg:reset postgres
```
Then recreate the database structure with
```
heroku run:detached python manage.py migrate
```

The firewall configuration also complicates the creation of the applications initial security principal (the "superuser"). Check the file named create_admin.sh.  It provides a method to create the superuser on heroku.
```
heroku run:detached bash ./create_admin.sh admin admin@example.com password
```

# Misc

You can see the deployed version at http://usma-it394-polls.herokuapp.com/polls/

## Reuse a Heroku Application Instance
Instead of creating a new Heroku application with "heroku create", You can associate a new clone of a project with an existing Heroku application instance.  I could clone this repository then associate it with the heroku application "immense-scrubland-9864" (previosly made with "heroku create" on another computer) with the following command:
```
heroku git:remote –a immense-scrubland-9864
```

## Procfile
Heroku uses the commands in the Procfile to run your application.  See https://devcenter.heroku.com/articles/procfile for additional information.