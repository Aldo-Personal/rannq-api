import hashlib
import hmac
import os
import redis
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session


class ApplicationConfig:

    redis_client = redis.Redis()

    SECRET_KEY = os.environ.get("SECRET_KEY")

    SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get(
        "SQLALCHEMY_TRACK_MODIFICATIONS")
    SQLALCHEMY_ECHO = os.environ.get("SQLALCHEMY_ECHO")
    SQLALCHEMY_POOL_SIZE = 20
    SQLALCHEMY_POOL_TIMEOUT = 3000
    SQLALCHEMY_POOL_RECYCLE = 36000
    RANNQ_API_KEY='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2NvdW50X2lkIjoiNjRlYzc3N2Y1MzdkZWIxNGEwMDZlZDM1Iiwic2VydmVyX2VudiI6IlByb2QiLCJzZXJ2ZXJfdXJsIjoiaHR0cHM6Ly9zZXJ2ZXIub25saW5lcmV2aWV3cy50ZWNoL2FwaS92MC4wLjkifQ.rQzAkXnWspWzT81XiF7LJAEUjR3znxxJ-MW371x5tnI'
    RAINEX_API_ID='7b795919e0db48d197bb12072ffa9c04'
    RAINEX_API_KEY='1VYBo1HAks7B1ghd4U1odaL9I4LJrRkqXUyJR5IZOp7M5E72BUbcxQbrWp6e05mb'

    # SQLALCHEMY_DATABASE_URI = r"sqlite:///./db.sqlite"
    username = os.environ.get("USERNAME")
    password = os.environ.get("PASSWORD")
    localhost = os.environ.get("LOCALHOST")
    dbname = os.environ.get("DBNAME")
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:E4bcd2d*g*afcF*D35C3F3fAbccafAEb@monorail.proxy.rlwy.net:23418/railway"

    DATABASE_ENGINE = create_engine(SQLALCHEMY_DATABASE_URI)
    SESSION_TYPE = os.environ.get("SESSION_TYPE")
    REDIS_URL = "redis://default:WrwSdqAH5iITwzhp8APu@containers-us-west-207.railway.app:6006"
    SESSION_REDIS = redis.from_url(REDIS_URL)
    SESSION_KEY_PREFIX = os.environ.get("SESSION_KEY_PREFIX")
    # SESSION_REDIS = redis_client
    SESSION_PERMANENT = os.environ.get("SESSION_PERMANENT")
    SESSION_USE_SIGNER = os.environ.get("SESSION_USE_SIGNER")
    PERMANENT_SESSION_LIFETIME = 86400

    MAIL_SERVER = 'smtp.elasticemail.com'
    MAIL_PORT = 2525
    MAIL_USERNAME = 'support@enetworksagencybanking.com.ng'
    MAIL_PASSWORD = "A2CDE2AB8EEE085BBF14DFF4D75315C7BF75"
    MAIL_USE_TLS = True

    DATABASE_INITIALIZED = False

    JWT_ACCESS_TOKEN_EXPIRES = 43200
