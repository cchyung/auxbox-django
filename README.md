# auxbox
## Description
A virtual jukebox.

# Setting up the Developer environment
1. Install virtualenv
2. `pip install -r requirements.txt`
3. In `venv/bin/activate`:
Set `DJANGO_SETTINGS_MODULE=auxbox.settings.local`
and set `SECRET_KEY=<secret_key>`
4. Create/install postgresql database for development, see settings for creds
5. `python manage.py migrate`
6. `python manage.py createsuperuser`
