FROM python:3.8.5-alpine
RUN pip install --upgrade pip
RUN apk add --no-cache gcc musl-dev linux-headers

WORKDIR /app

COPY . /app
RUN pip install -r requirements.txt

RUN chmod +x entrypoint.sh
ENTRYPOINT [ "sh" , "entrypoint.sh" ]


