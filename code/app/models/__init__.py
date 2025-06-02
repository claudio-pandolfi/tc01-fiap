from mongoengine import connect

def register_db_connection(app):
    # connect(app.config['MONGODB_DATABASE'], host=app.config['MONGODB_HOST'], port=app.config['MONGODB_PORT'])
    connect(host=app.config['MONGODB_HOST'])
