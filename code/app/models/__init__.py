from mongoengine import connect

def register_db_connection(app):
    connect(host=app.config['MONGODB_HOST'])
