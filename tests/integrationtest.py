import unittest
import requests
from .app import Expression

class IntergrationTest(unittest.TestCase):

    def test_right_expression(self):
        expression = "1 + 1"
        r = requests.post('http://web:5000', data = {'expression':expression})
        inserted = Expression.query.filter(text=expression).first()
        self.assertEqual(inserted.text, expression)

    def test_wrong_expression(self):
        expression = "12 ++ 2"
        r = requests.post('http://web:5000', data = {'expression':expression})
        inserted = Expression.query.filter(text=expression).first()
        self.assertEqual(inserted, None)

#dockerfile:

RUN python ../tests.py

#docker-compose
version: "3.3"
services:
  test:
    image: test
    build: .:/integration
    links:
      - web
    networks:
      - webnet
  web:
    image: cs162-flask
    depends_on:
      - db
    deploy:
      replicas: 4
      resources:
        limits:
          cpus: "0.2"
          memory: 64M
      restart_policy:
        condition: "on-failure"
    ports:
      - 5000:5000
    networks:
      - webnet
    volumes:
      - .:/app

  db:
    image: postgres:alpine
    ports:
    - 5432:5432
    environment:
      POSTGRES_DB: "cs162"
      POSTGRES_USER: "cs162_user"
      POSTGRES_PASSWORD: "cs162_password"
    networks:
      - webnet
    deploy:
      restart_policy:
        condition: "on-failure"

  adminer:
    image: adminer
    depends_on:
      - db
    deploy:
      restart_policy:
        condition: "on-failure"
    ports:
      - 8080:8080
    networks:
      - webnet
networks:
  webnet: