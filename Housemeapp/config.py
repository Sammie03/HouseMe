class Config(object): #contains configs common to all
    ADMIN_EMAIL="info@houseme.com"
    USERNAME = "Houseme"
    
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI="mysql+mysqlconnector://root@127.0.0.1/Houseme"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    
    MERCHANT_ID = "t98765@0"
    
class TestConfig(Config):
    DATABASE_URL = "Test Connection Parameters"

