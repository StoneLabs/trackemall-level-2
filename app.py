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

@app.route("/getDetection", methods=['GET'])
def getDetection():
    return mc.get_object("fframes", str(request.args.get("id")))

@app.route("/getNext", methods=['GET'])
def getNext():
    objects = mc.list_objects_v2('frames')
    x = []
    for obj in objects:
        x.append(int(obj.object_name.encode('utf-8')))
    return objects[objects.index(sorted(x)[0])]

@app.route("/setDetection", methods=['POST'])
def setDetection():
    identifier = request.data("id")
    frame = request.data("blob")
    f = open("tmp/n"+str(identifier), "w")
    f.write(str(frame))
    f.close()
    mc.fput_object("fframes", str(identifier), "tmp/n"+str(identifier), "text/plain")
    os.remove("tmp/n"+str(identifier))
    return 


@app.route("/addFrame", methods=['POST'])
def addFrame():
    f = request.files['file']
    counter = request.args.get("id")
    f.save('/tmp/o'+str(counter))
    mc.fput_object("frames", str(counter), "/tmp/o"+str(counter), "text/plain")
    os.remove("/tmp/o"+str(counter))
    return str("fuuuck")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2438, debug=True)
