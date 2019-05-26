from Algo2 import Algo2

def testAlgoWithQuestions():
    algo = Algo2()
    while True:
        # print(algo.getNumOfRelevantDishes())
        name = algo.getNextAtt()
        ans = input('got ' + name + '?\n')
        res = {'name':name, 'ans':ans}

        x = algo.respond(res)
        print(x)
        if x:
            print(algo.recPreview())
            break


# algo2 = Algo2()
#
# x = algo2.getNextAtt()
# print(x)
# algo2.respond()
testAlgoWithQuestions()