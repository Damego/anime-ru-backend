from os import environ

from .client import PostgresClient

postgres = PostgresClient(
    host=environ["POSTGRES_HOST"],
    user=environ["POSTGRES_USER"],
    password=environ["POSTGRES_PASSWORD"]
)
