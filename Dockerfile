# ---- Base Node ----
#Python and Linux version
FROM python:3.9 AS base
RUN apt-get update -y
RUN apt-get install -y fluidsynth-dssi fluidsynth
ARG app_home=/app
ENV APP_HOME $app_home
WORKDIR ${APP_HOME}
COPY ./requirements.txt ${APP_HOME}
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . ${APP_HOME}/
#TO RUN IN LOCAL UNCOMMENT THESE
 EXPOSE 8000
# The number of worker processes for handling requests. --workers
 CMD ["gunicorn", "--bind", ":8000", "--workers", "2", "Music_Generation_System.wsgi:application"]
 
#FOR HEROKU DEPLOYMENT
#CMD gunicorn Music_Generation_System.wsgi:application --bind 0.0.0.0:$PORT
