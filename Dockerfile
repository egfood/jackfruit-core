FROM python:3.9.1
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
ENV PORT 8000
COPY . /code/
CMD ./start-app.sh
