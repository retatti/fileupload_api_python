FROM python:3

WORKDIR /app

RUN apt-get update
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools

COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt


# CMD [ "python", "./your-daemon-or-script.py" ]
CMD [ "sh" ]
