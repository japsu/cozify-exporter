FROM python:3.8
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY requirements.txt /usr/src/app/
RUN pip install -U pip setuptools wheel && pip install -r requirements.txt
ENV FLASK_APP=cozify_exporter.py
COPY cozify_exporter.py /usr/src/app/
CMD ["flask", "run", "--host=0.0.0.0"]
