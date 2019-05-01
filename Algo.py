import csv
import threading


class Algo():

    #nextAtt= None;

    def __init__(self):
        print("init algo object")
        datasize = "1000data"  # fulldata || 1000data
        # TODO: write code for the case the file doesnt found
        self.data_file = open('./' + datasize + '/data.csv', newline='')
        self.attr_file = open('./' + datasize + '/attNames.csv')
        self.dishes_file = open('./' + datasize + '/DishesIds.csv')

        self.AttArr = self.attr_file.readline().split(',')
        self.DishesArr = self.dishes_file.readline().split(',')

        self.DISHES_THRESHOLD = 10
        self.NUMBER_OF_ATTR = len(self.AttArr)
        self.NUMBER_OF_DISHES = len(self.DishesArr)
        self.lock = threading.Lock()

        # init empty gini-rates list with none
        self.giniRates = [None] * self.NUMBER_OF_ATTR

        # init Relevant Rows arr
        self.RR = [1] * self.NUMBER_OF_ATTR

        # init Relevant columns arr
        self.RC = [1] * self.NUMBER_OF_DISHES

        self.NumberOfRelevantAtt = self.NUMBER_OF_ATTR

        self.reader = csv.reader(self.data_file, delimiter=',', quotechar='|')

        self.indexAttWithMaxGini=-1

        self.lock.acquire()
        self.calcTheNextAtt() # this function update the 'nextAtt' var
        self.lock.release()

    def calcGini(self,no, yes):
        return 1 - (yes / self.NUMBER_OF_DISHES) ** 2 - (no / self.NUMBER_OF_DISHES) ** 2

    def ReadSpecificLine(self,lineNumber, file):
        file.seek(0)
        for i, line in enumerate(file):
            if i == lineNumber:
                return line
        return "ERROR: LINE #" + str(lineNumber) + " DOESN'T FOUND"

    def AreWeFinish(self):
        return True if sum(self.RC) <= self.DISHES_THRESHOLD else False

    def AND(self,A, B):
        leng = len(A)
        for i in range(0, leng):
            if A[i] == 1 & B[i] == 1:
                A[i] = 1
            else:
                A[i] = 0
        return A

    def getNumOfRelevantDishes(self):
        return self.NUMBER_OF_DISHES

# this method calc which att will be ask next and update the global var 'nextAtt'
    def calcTheNextAtt(self):

        while (self.AreWeFinish() == False):

            # return for the file start
            self.data_file.seek(0)

            i = 0
            for row in self.reader:
                # If the Row in relevant
                if self.RR[i]:
                    yesCount = 0
                    noCount = 0
                    j = 0
                    for cell in row:
                        if self.RC[j]:
                            if cell == '0':
                                noCount += 1
                            else:
                                yesCount += 1
                        j += 1
                    self.giniRates[i] = self.calcGini(noCount, yesCount)
                # the else section can be remove for optimize the performers
                else:
                    self.giniRates[i] = -1
                # print section : for dev
                # print(str(row) + str(RR[i]) + "  " + AttArr[i] + "  zero:" + str(noCount) + "  one:" + str(yesCount) +
                #       "  Gini Rate:  " + str(giniRates[i]))
                i += 1

            # TODO: random attr choices effected by this line
            # return first instance of the largest valued
            self.indexAttWithMaxGini = self.giniRates.index(max(self.giniRates))
            self.attWithMaxGini = self.AttArr[self.indexAttWithMaxGini]

            self.nextAtt = self.attWithMaxGini
            return


# this method get the respond for the ask att
    def respon(self,answer):
        self.lock.acquire()

        if answer == "0":
            print("algo:i dont have " + self.attWithMaxGini)
            self.NumberOfRelevantAtt = self.NumberOfRelevantAtt - 1
            # update the relevant dishes arr
            # this pip line: read-line-> split -> to int -> inverse 0>1 & 1>0
            reverseRow = list(map((lambda x: 1 if x == 0 else 0),
                                  [int(x) for x in self.ReadSpecificLine(self.indexAttWithMaxGini, self.data_file).split(',')]))
            self.RC = self.AND(self.RC, reverseRow)
            NUMBER_OF_DISHES = sum(self.RC)


        if answer == "1":
            print("algo:i have " + self.attWithMaxGini)

        # the section run after we update the arrays with the answer that we get from the client

        self.calcTheNextAtt()
        self.lock.release()



    def getNextAtt(self):
        return self.nextAtt;