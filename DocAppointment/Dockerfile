FROM python:3.12-alpine

ENV PYTHONWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install -r requirements.txt

COPY . ./code

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]