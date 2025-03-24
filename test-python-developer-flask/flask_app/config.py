import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "supersecretkey")
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:RNYBagpqfzLJgpfAqoXkofxqgBTqNvAd@shortline.proxy.rlwy.net:32828/railway"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_TYPE = 'filesystem'
    WTF_CSRF_ENABLED = True
