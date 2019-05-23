import json
from time import sleep

from Algo import Algo
import requests

local = 'http://127.0.0.1'
server = 'http://132.145.27.181'
preview = '/get-preview-info'
nextAtt = '/get-next-att'
restart = '/restart-algo'
yesNo = '/send-yes-or-no'
yes = json.dumps({"res": "1"})
no = json.dumps({"res": "0"})


def testURL(machine):
    if machine == 'local':
        machine = local
    else:
        if machine == 'server':
            machine = server

    requests.get(machine + restart)
    reslist = [yes, no, no, no, no, no, yes]  # responses list can be changed to test different scenarios
    r = reslist[0]
    print(requests.get(machine + nextAtt).json())
    ryesNo = requests.post(machine + yesNo, r).json()

    print(ryesNo)
    for r in reslist[1:]:
        while ryesNo['areWeFinish'] == 0:
            print(requests.get(machine + nextAtt).json())
            ryesNo = requests.post(machine + yesNo, yes).json()
            print(ryesNo)

        rpreview = requests.get(machine + preview).json()
        print(rpreview)
        break


def testAlgoWithNoQuestions():
    reslist = ['1', '0', '0', '0', '0', '0', '1']  # responses list can be changed to test different scenarios
    algo = Algo()
    r = reslist[0]  # init r to the first response
    print(algo.getNumOfRelevantDishes())
    print(algo.getNextAtt())
    res = algo.respon(r)
    for r in reslist[1:]:  # starts the responses list from the 2nd position
        while not res:  # while the response is that we are not finished
            print(algo.getNextAtt())
            print(algo.getNumOfRelevantDishes())
            res = algo.respon(r)
        print(algo.getPreviewInfo())
        break


def testAlgoWithQuestions():
    algo = Algo()
    while True:
        while True:
            print(algo.getNumOfRelevantDishes())
            if (algo.respon(input('got ' + algo.getNextAtt() + '?\n'))):
                break
        print(algo.getPreviewInfo())
        algo = Algo()


testURL('server') # choose if you want server or local machine
testAlgoWithNoQuestions()
# testAlgoWithQuestions()
