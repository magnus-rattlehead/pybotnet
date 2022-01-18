###########
# BUILDER #
###########

# pull official base image
FROM python:3.9-alpine as builder

# set work directory
WORKDIR /usr/src/billygates

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

# lint
RUN pip install --upgrade pip
RUN pip install flake8
COPY . .
RUN flake8 --ignore=E501,F401 .

# install dependencies
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/billygates/wheels -r requirements.txt


#########
# FINAL #
#########

# pull official base image
FROM python:3.9-alpine

# create directory for the app user
RUN mkdir -p /home/billygates

# create the app user
RUN addgroup -S billygates && adduser -S billygates -G billygates

# create the appropriate directories
ENV HOME=/home/billygates
ENV APP_HOME=/home/billygates/billygates
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/static
WORKDIR $APP_HOME

# install dependencies
RUN apk update && apk add libpq
COPY --from=builder /usr/src/billygates/wheels /wheels
COPY --from=builder /usr/src/billygates/requirements.txt .
RUN pip install --no-cache /wheels/*


# copy project
COPY . $APP_HOME

# chown all the files to the app user
RUN chown -R billygates:billygates $APP_HOME

# change to the app user
USER billygates
