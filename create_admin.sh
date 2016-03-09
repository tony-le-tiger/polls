 #!/usr/bin/env bash
 # Use this to create a new Django administrative user on Heroku after database migrations are complete.
 # The local network configuration blocks port 5000, which is needed to run
 # heroku one-off dynos interactively.
 # 
 # To create a user named "admin", with e-mail "admin@example.com" and password of "password" enter the 
 # following:
 #
 #   heroku run:detached bash ./create_admin.sh admin admin@example.com password
 #
 # Original concept from http://source.mihelac.org/2009/10/23/django-avoiding-typing-password-for-superuser/
 #
 echo "from django.contrib.auth.models import User; User.objects.create_superuser('$1', '$2', '$3')" |  python manage.py shell
