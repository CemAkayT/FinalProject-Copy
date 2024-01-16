FROM python:3.11.1
WORKDIR /hovedopgave
COPY . .
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["flask", "run", "--host", "0.0.0.0"]