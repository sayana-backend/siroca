#FROM python:3.10
#
#ENV PYTHONWRITEBYTECODE 1
#
#WORKDIR /project
#
#COPY requirements.txt /project/requirements.txt
#
#RUN pip install -r /project/requirements.txt
#
#COPY . /project/


FROM python:3.11
WORKDIR /usr/src/app
COPY requirements.txt ./
COPY . .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt && python manage.py collectstatic --noinput
