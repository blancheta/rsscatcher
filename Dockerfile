FROM python:3.5
ENV PYTHONUNBUFFERED 1

ENV APP_USER user
ENV APP_ROOT /src

RUN mkdir /config
ADD /config/requirements.pip /config/
RUN pip install -r /config/requirements.pip
WORKDIR /src
