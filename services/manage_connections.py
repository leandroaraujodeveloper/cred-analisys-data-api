import os
import contextlib

import psycopg2

import pymongo
from pymongo import MongoClient

from elasticsearch import Elasticsearch

from dotenv import load_dotenv

from nameko.rpc import rpc, RpcProxy

import json

load_dotenv()

@contextlib.contextmanager
def get_postgres_connection(database):
    """
    Context manager para gerenciar a conexão com o banco de dados Postgresql
    """
    connection = psycopg2.connect(host=os.getenv('A_CONSUMER_HOST'),
                                database=database,
                                user=os.getenv('A_CONSUMER_USER'),
                                password=os.getenv('A_CONSUMER_PWD'))

    try:
        yield connection
    finally:
        connection.close()

@contextlib.contextmanager
def get_mongo_connection(database):
    client = MongoClient()
    client = MongoClient(os.getenv('B_RATING_URI'))
    connection = client[database]
    yield connection

@contextlib.contextmanager
def get_elaticsearch_connection(index):
    client = Elasticsearch([os.getenv('C_TRANSACTIONS_URI')])

import manage_connections as m_conn
import pandas as pd

class DataSourceService:
    name = 'manage_connections'

    zipcode_rpc = RpcProxy('connectionsservice')

    @rpc
    def get_datasources(self, database):
        with m_conn.get_mongo_connection('B_RATING') as conn:
            data = conn.B_RATING.find()
            result = []
            for row in data:
                result.append(row)
            return str(result)
