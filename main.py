import os
from flask import Flask, request, jsonify, render_template
from flask_restful import Resource, Api

from protopost import protopost_client as ppcl
from nd_to_json import nd_to_json, json_to_nd

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

import signal
signal.signal(signal.SIGTERM, lambda: exit(0))

PORT = os.getenv("PORT", 80)

app = Flask(__name__)
api = Api(app)

@app.route("/")
def index():
    return render_template("index.html")

class GetData(Resource):
    def post(self):
        #get url
        url = request.get_json(force=True)
        #get data from url
        data = ppcl(url)
        try:
          data = json_to_nd(data)
          print(data)
        except:
          print("couldnt parse data as nd array")

        #send as simple json object
        data = nd_to_json(data, method="plain")
        return data

api.add_resource(GetData, "/getData")

app.run(host="0.0.0.0", port=PORT)
