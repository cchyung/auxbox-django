# auxbox
## Description
A project for a virtual jukebox that allows users to submit requests to queue, and vote on other people's requests.  Perfect for a party, a roadtrip with friends, or a restaurant trying to allow for customer requests.

# Setting up the Developer environment
1. Install virtualenv
2. `pip install -r requirements.txt`
3. In `venv/bin/activate`: set `DJANGO_SETTINGS_MODULE=auxbox.settings.local`
and set `SECRET_KEY=<secret_key>`
4. Create/install postgresql database for development, see settings for creds
5. `python manage.py migrate`
6. `python manage.py createsuperuser`
