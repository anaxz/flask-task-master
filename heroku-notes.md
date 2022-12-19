git init
git add .
heroku create repo-name
git remote -v
git push keroku master

touch Procfile
> inside file put:
web: gunicorn app:app
- this is to tell heroku to make webserver at
- above works for non-windows? use waitress?

To relaunch to heroku, must git add everything again. 

ref: https://www.youtube.com/watch?v=Z1RJmh_OqeA