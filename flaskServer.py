from flask import Flask, request, jsonify

import json
from Algo import Algo



app = Flask('what2eat')

global algo
algo =Algo()

# Decorator defines a route
# http://localhost:5000/
@app.route('/')
def index():
    return "Hello Wrld!"

@app.route('/send-yes-or-no',methods=['POST'])
def getYESorNO():
    data = request.data.decode('utf-8')
    res = json.loads(data)['res']

    print("server:call to algo.respon with:"+str(res))
    algo.respon(res)
    return "<h1>OK</h1>"

@app.route('/get-next-att',methods=['GET'])
def sendAtt():
    print("The server send:"+str(algo.getNextAtt()));
    print(algo.getNumOfRelevantDishes())
    return jsonify(
        nextAtt=algo.getNextAtt(),
        numOfRelevantDishes=algo.getNumOfRelevantDishes()
        ) # return json



if __name__ == '__main__':
    app.debug = True
    app.run(host='10.100.102.2', port=5005)
    #app.run(host='10.200.203.231',port=5005)