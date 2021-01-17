FROM python:alpine

COPY app.py .

RUN pip3 install Flask beautifulsoup4 requests && chmod +x app.py

ENTRYPOINT [ "/app.py" ]