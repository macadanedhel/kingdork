FROM python:alpine3.7
WORKDIR /home/kingdork
COPY requirements.txt /home/kingdork
COPY kingdork.py /home/kingdork
RUN pip install --no-cache-dir -r /home/kingdork/requirements.txt