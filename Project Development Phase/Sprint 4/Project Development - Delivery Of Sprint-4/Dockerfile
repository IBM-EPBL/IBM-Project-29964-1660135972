FROM python:alpine3.11
LABEL maintainer="Raagul Sridharan, raagulsridharan01@gmail.com"
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
CMD [ "python", "-m" , "flask", "--debug", "run"]