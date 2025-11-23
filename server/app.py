from flask import Flask

app=Flask(__name__)

@app.route('/')
def home():
    #basic route to test server
    return{'message':'Welcome to the Late Show API'}

if __name__=='__main__':
    #run the port on app 5555
    app.run(port=5555, debug=True)