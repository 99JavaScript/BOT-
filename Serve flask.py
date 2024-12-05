from flask import flask
from threading import Thread

app = Flask('')

@app.route9('/')
def home():
     return "Server is runing!"

def run():
      app.run(host='0.0.0.',port=8080)

      def server_on():
             t = Thread(target=run)
             t.start()
            