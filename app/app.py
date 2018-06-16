import os
from flask import Flask, request
from flask_cors import CORS
from minio import Minio

app = Flask(__name__)

CORS(app)

mc = Minio("minio:9000", access_key="belastend", secret_key="belastend42", secure=False)

try:
    mc.make_bucket("frames")
    mc.make_bucket("fframes")
except:
    print("fuck")

counter = 0

@app.route("/getDetection")
def getDetection():
    return mc.get_object("fframes", str(request.data("id")))

@app.route("/getNext")
def getNext(id):
    return mc.get_object("frames", str(counter))


@app.route("/setDetection")
def setDetection():
    identifier = request.data("id")
    frame = request.data("blob")
    f = open("tmp/n"+str(identifier), "w")
    f.write(str(frame))
    f.close()
    mc.fput_object("fframes", str(identifier), "tmp/n"+str(identifier), "text/plain")
    os.remove("tmp/n"+str(identifier))
    return 


@app.route("/addFrame")
def addFrame():
    frame = request.data("blob")
    f = open("tmp/o"+str(counter), "w")
    f.write(str(frame))
    f.close()
    mc.fput_object("frames", str(counter), "tmp/o"+str(counter), "text/plain")
    os.remove("tmp/o"+str(counter))
    counter += 1
    return "success"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2438, debug=True)
