import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg2://career_user:career_pass@localhost:5432/career_guide_ai"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret_key")

class DevConfig(Config):
    DEBUG = True

class ProdConfig(Config):
    DEBUG = False
