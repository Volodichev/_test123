FROM python:3.10.7-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /lave_test
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
#RUN ["chmod", "+x", "docker-entrypoint.sh"]
#ENTRYPOINT [ "./docker-entrypoint.sh" ]
CMD [ "/bin/bash", "-c", "python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000" ]