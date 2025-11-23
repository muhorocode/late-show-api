from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api

#initialize flask app
app=Flask(__name__)

#configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False

#initialize extensions
db=SQLAlchemy(app)
migrate=Migrate(app,db)
api=Api(app)

@app.route('/')
def home():
    #basic route to test server
    return{'message':'Welcome to the Late Show API'}

if __name__=='__main__':
    #run the port on app 5555
    app.run(port=5555, debug=True)