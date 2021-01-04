FROM python:3.8
ENV PYTHONUNBUFFERED 1
WORKDIR /code
COPY requirements_prod.txt /code/
RUN pip install -r requirements_prod.txt
ENV PORT 8000
COPY . /code/
CMD daphne -b 0.0.0.0 -p $PORT core.asgi:application