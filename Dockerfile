FROM python:3.6-stretch
COPY services /services
WORKDIR /services
ENV FLASK_APP=api.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV PYTHONPATH="${PYTHONPATH}:/cred_analisys_api"
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["flask", "run"]
RUN nameko run services.manage_connections:DataSourceService

