FROM python:3.8

WORKDIR /dj_app

COPY ./django /djgango

RUN pip install -r /django/requirements.txt

ENV SECRET_KEY hlfaueoiwyr876987yiaUyu&^*((*98oivfjsodri0(*_)-0))
ENV DEBUG 1

RUN python manage.py migrate

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "stocks_products.wsgi"]
