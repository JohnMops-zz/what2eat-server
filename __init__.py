import sys
import os
import threading
from time import sleep

from flask import Flask, request, jsonify, render_template

import json
from .Algo2 import Algo2

app = Flask(__name__)
# global algo
algos = dict()


@app.route('/')
def index():
      return render_template('page.html')

@app.route('/run-algo',methods=['GET'])
def runAlgo():
    print("inside Run-algo")
    algo = Algo2()
    algos[id(algo)]=algo
    return jsonify(
        algoId=id(algo)
        ) # return json


@app.route('/send-yes-or-no',methods=['POST'])
def sendYesOrNo():
    data = request.data.decode('utf-8')

    res = json.loads(data)
    print("server: call to algo.respond with:"+str(res))
    algoId=res["algoId"]
    resp = algos[algoId].respond(res)
    return jsonify(
        areWeDone=resp
        ) # return json

@app.route('/get-next-att',methods=['POST'])
def getNextAtt():
    
    data = request.data.decode('utf-8')
    res = json.loads(data)

    algoId = res["algoId"]
    if algoId in algos:
        attRes=algos[algoId].getAtt()
        print("str(algos)="+str(algos)+" "+str(id(algos)))
    else:
        raise Exception('Key-ERR'+str(algos)+" "+str(algoId)+" "+str(id(algos)))

    name=attRes["name"]
    relRecs=attRes["relRecs"]
    attImgUrl=attRes["img"]
    print("The server sent: "+name)
    print("Relevant recipes: "+str(relRecs))

    return jsonify(
        nextAtt=name,
        numOfRelevantDishes=relRecs,
        nextAttImage=attImgUrl
        ) # return json

@app.route('/get-preview-info',methods=['POST'])
def getPreviewInfo():
    
    data = request.data.decode('utf-8')
    res = json.loads(data)
    algoId = res["algoId"]
    recPreview=algos[algoId].getRecPreview()
    print("deleting algo obj with id "+str(algoId))
    del algos[algoId]
    return jsonify(
        recPreviewInfo=recPreview
    )

if __name__ == '__main__':

    app.run(host='127.0.0.1',port='80')
    # app.run(host='10.200.203.231',port=5005)