class DatabaseConfig:
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:a1234567@localhost/RMS"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    REDIS_URL = "redis://@localhost:6379/0"
