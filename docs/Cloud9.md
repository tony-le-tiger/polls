# Cloud9 Setup
If you are interested in trying a SaaS IDE I recommend trying Cloud9.
You can sign up for an account at https://c9.io
The basic free account is probably enough to run your IT394 course project for
development purposes.

# Starting out
After you've signed up for Cloud9 start a new project that clones your current project
work from GitHub.  You'll need to do some configuration of the Unix environment
that is running in the Docker instance
(as user ubuntu) 
```
sudo su
```
(as user root)
```
pip install -r requirements.txt 
pip install coverage
service postgresql start
su - postgres
```
(as user postgres)
Create a PostgreSQL user named ubuntu, create a database (I'm using 'polls') for
your project, and finally make ubuntu the owner of the database.


```
#cloud9 postgres is configured to use peer authentication from the localhost
#check the pg_hba.conf for details.
# you can find the pg_hba.conf with:
# find / -name pg_hba.conf

createuser -dslP ubuntu
createdb --owner=ubuntu polls
exit
```
(as user ubuntu)
```
export DATABASE_URL="postgres://ubuntu:password@localhost:5432/polls"
```

You can make the environment variable persistent with:
```
echo "export DATABASE_URL='postgres://ubuntu:password@localhost:5432/polls'" >> ~/.profile
```
