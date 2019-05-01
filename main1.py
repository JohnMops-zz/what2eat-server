import csv

DISHES_THRESHOLD = 1
NUMBER_OF_ATTR = 2251 # ROW=ATTR
NUMBER_OF_DISHES = 10 # DISH = COLUMN
NumberOfRelevantAtt = 10

def calcGini(no,yes):
    return 1 - (yes / NUMBER_OF_DISHES) ** 2 - (no / NUMBER_OF_DISHES) ** 2

def ReadSpecificLine(lineNumber,file):
    file.seek(0)
    for i, line in enumerate(file):
        if i == lineNumber:
            return line
    return "ERROR: LINE #"+str(lineNumber)+" DOESN'T FOUND"

def AreWeFinish():
    return True if sum(RC) <= DISHES_THRESHOLD else False


# TODO: write code for the case the file doesnt found
data_file = open('TransRecipesUtf8.csv',newline='')
attr_file = open('attNames.csv')
dishes_file = open('DishesIds.csv')

AttArr = attr_file.readline().split(',')


# init empty gini-rates list with none
giniRates = [None]*NUMBER_OF_ATTR

# init Relevant Rows arr
RR = [1]*NUMBER_OF_ATTR

# init Relevant columns arr
RC = [1]*NUMBER_OF_DISHES

reader = csv.reader(data_file, delimiter=',', quotechar='|')

while(AreWeFinish()==False):
    # return for the file start
    data_file.seek(0)

    print("NUMBER_OF_DISHES: "+str(NUMBER_OF_DISHES))
    print(RC)
    i = 0
    for row in reader:
        # If the Row in relevant
        if RR[i]:
            yesCount = 0
            noCount = 0
            j=0
            for cell in row:
                if RC[j]:
                    if cell == '0':
                        noCount += 1
                    else:
                        yesCount += 1
                j +=1
            giniRates[i] = calcGini(noCount, yesCount)
        # the else section can be remove for optimize the performers
        else:
            giniRates[i]=-1
        # print section : for dev
        print(str(row) + str(RR[i]) + "  " + AttArr[i] + "  Gini Rate:  " + str(giniRates[i]))
        i += 1

    # TODO: random attr choices effected by this line
    # return first instance of the largest valued
    indexAttWithMaxGini = giniRates.index(max(giniRates))
    attWithMaxGini  = AttArr[indexAttWithMaxGini]

    print(attWithMaxGini+ "?")
    answer = input()
    if answer == "0":
        print("i dont have "+attWithMaxGini)
        NumberOfRelevantAtt = NumberOfRelevantAtt-1

        # update the relevant dishes arr
        # this pip line: read-line-> split -> to int -> inverse 0>1 & 1>0
        reverseRow = list(map((lambda x: 1 if x == 0 else 0), [int(x) for x in ReadSpecificLine(indexAttWithMaxGini, data_file).split(',')]))
        RC = RC and reverseRow
        NUMBER_OF_DISHES = sum(RC)
    else:
        print("i have "+attWithMaxGini)
    RR[indexAttWithMaxGini] = 0  # mark as used attr

print("DONE !")
