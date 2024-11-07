class DatabaseConfig:
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:a1234567@localhost/RMS"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    REDIS_URL = "redis://:qweasd123@localhost:63799/0"
