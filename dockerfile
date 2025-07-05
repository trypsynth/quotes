FROM python:3.10-alpine3.14
WORKDIR /srv
COPY . /srv
RUN pip install --upgrade pip
RUN pip install uv
ENV FLASK_APP=app
CMD ["uv","run","app.py"]
