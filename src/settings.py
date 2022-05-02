import os
from turtle import dot
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')

class Config:
    CONN_STRING = os.getenv('CONN_STRING')
    TARGET_SCHEMA = os.getenv('TARGET_SCHEMA')
    DATAPATH = "data/"