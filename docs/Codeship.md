# Codeship
Codeship is a Continuous Delivery system.  See https://codeship.com for more
information.

#Project Settings
Below Project Settings so the testing will use PostgreSQL on 
Codeship that will work with the DATABASE_URL technique.

##Test
###Setup Commands
```
# Setup PostgreSQL 9.3
#https://codeship.com/documentation/databases/postgresql/
export PG_DBNAME='polls'
createdb --owner=$PG_USER $PG_DBNAME
export DATABASE_URL="postgres://$PG_USER:$PG_PASSWORD@127.0.0.1:5432/$PG_DBNAME"

pip install -r requirements.txt

# Sync your DB for django projects
# python manage.py syncdb --noinput
# Run migrations for your django project
# python manage.py migrate --noinput
```

###Test Commands
```
# Running your Django tests
python manage.py test

# You can also run your own python scripts
# python run_tests.py
# Or use fabric to run your tests
# fab test
```

##Deployment
I set up a deployment pipeline for Heroku.  A couple of things to check:
You might have to explicitly set the URL for the application.   Also, turn off
"Run migrations" option since it only runs rake migragtions for Ruby on Rails.

