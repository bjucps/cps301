# To use this app:
#   pip install flask

from flask import Flask, request
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def hello():
    if 'name' in request.args:
        name = request.args['name']
    else:
        name = "world"
    return f"""<html><body>
        <h1>Hello, {name}!</h1>
        The time is {datetime.now()}.</body></html>"""

# Launch the local web server
if __name__ == "__main__":
    app.run(host='localhost', debug=True)
    
