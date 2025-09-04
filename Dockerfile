FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update && \
apt-get install -y --no-install-recommends netcat-openbsd && \
rm -rf /var/lib/apt/lists/*

# copy and install python dependencies

COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

#Copy project files

COPY . /app/

# entrypoint script (will wait for db and run migrations)

COPY ./entrypoint.sh /entrypoint.sh

RUN chmod +x entrypoint.sh

#Expose application port
EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]

CMD ["gunicorn", "BlissBasket.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
