FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir openapi
COPY openapi/FSCATAPI.json ./openapi/
COPY ss.py ./
COPY util.py ./
COPY app.py ./

CMD [ "python", "./app.py" ]

# docker build -t saticatapibnr .
# docker run -it --rm -p 8080:8080 --name saticatapibnr saticatapibnr