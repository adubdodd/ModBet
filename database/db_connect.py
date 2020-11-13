import pandas as pd
import configparser
import sqlalchemy as db

def create_connection():
    config = configparser.ConfigParser()
    config.read('credentials.txt')
    DB_URI = ''.join(['postgres+psycopg2://',remote['user'],':',remote['password'],'@',remote['server'],'/',remote['database']])
    return db.create_engine(DB_URI).connect()