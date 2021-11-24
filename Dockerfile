FROM python:3.8-slim

RUN mkdir /plextime-scripts

ADD setup.py /plextime-scripts
ADD start.py /plextime-scripts
ADD src /plextime-scripts/src

RUN cd /plextime-scripts && pip install --no-cache-dir .

WORKDIR /plextime-scripts

CMD ["python", "start.py"]
