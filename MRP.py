import sqlite3
from operations.EOQ_EPQ import eoq, epq

'''
    MRP排程
    逐批訂購法 P.425
    input: 毛需求( MPS() ), 時間
'''
def mrp(month, car):
    mrpTable = print(generateProduceOrder(month, car)[0]) + print(generateBuyOrder(month, car))
    return mrpTable

def generateProduceOrder(time, car):
    conn = sqlite3.connect('FinalPro.db')
    # Purchase Order
    demand = epq(car)
    purchaseOrder = []
    purchaseOrder.append(["%s(月)" % time, "0.5\t1\t1.5\t2\t2.5\t3\t3.5\t4(週)"])
    opSche = []
    #opSche.append([""])

    # Get assembly time
    cursorA = conn.execute("select Assembly_Time from main.Product where Product_Name = '%s'" % car)
    for row in cursorA:
        assemblyTime = float(row[0])
    sendOrderTime = 4 - assemblyTime
    opSche.append(["組裝", assemblyTime, sendOrderTime, 4])
    purchaseOrder.append(["組裝", sendOrder(sendOrderTime, demand)])

    i = ""
    if car == "Car 1":
        i = '1'
    elif car == "Car2":
        i = '2'
    cursorP = conn.execute("select Part_ID, Preparing_Time from main.Supply where Part_ID like 'P{}%'".format(i))
    for row in cursorP:
        id = row[0]
        preTime = float(row[1])
        name = getLayerPartData(id)[0]
        amount = getLayerPartData(id)[1] * demand
        dueTime = 4 - assemblyTime
        # layer 1
        if id[2] == '1':
            sendOrderTime = dueTime - preTime
        # layer 2
        '''
        elif id[2] == '2':
            n = id[3:5]
            toptime = 0
            cursor = conn.execute("select Preparing_Time from main.Supply where Part_ID like 'P{}1{}00'".format(i, n))
            for row in cursor:
                toptime = row[0]
            sendOrderTime = dueTime - toptime - preTime
        '''
        purchaseOrder.append([name, sendOrder(sendOrderTime, amount)])
        opSche.append([name, preTime, sendOrderTime, float(dueTime)])
    conn.close()
    return purchaseOrder, opSche

def generateBuyOrder(time, car):
    conn = sqlite3.connect('FinalPro.db')
    # Purchase Order
    demand = eoq(car)
    buyOrder = []

    # Get assembly time
    cursorA = conn.execute("select Assembly_Time from main.Product where Product_Name = '%s'" % car)
    for row in cursorA:
        assemblyTime = row[0]
    sendOrderTime = 4 - assemblyTime

    i = ""
    if car == "Car 1":
        i = '1'
    elif car == "Car 2":
        i = '2'
    cursorP = conn.execute("select Part_ID, Preparing_Time from main.Supply where Part_ID like 'B{}%'".format(i))
    for row in cursorP:
        id = row[0]
        preTime = row[1]
        name = getLayerPartData(id)[0]
        amount = getLayerPartData(id)[1] * demand
        sendOrderTime = 4 - assemblyTime
        # layer 1
        if id[2] == '1':
            sendOrderTime = sendOrderTime - preTime
            buyOrder.append([name, sendOrder(sendOrderTime, amount)])
        elif id[2] == '2':
            n = id[3:5]
            toptime = 0
            cursor = conn.execute("select Preparing_Time from main.Supply where Part_ID like 'B_2{}00'".format(n))
            for row in cursor:
                toptime = row[0]
            sendOrderTime = sendOrderTime - toptime - preTime
            buyOrder.append([name, sendOrder(sendOrderTime, amount)])
    conn.close()
    return buyOrder

def getLayerPartData(id):
    conn = sqlite3.connect("FinalPro.db")
    cursor = conn.execute("select Part_Name, Part_Included from main.Part where Part_ID = '{}'".format(id))
    for row in cursor:
        name = row[0]
        amount = row[1]
    conn.close()
    return [name, amount]

def sendOrder(time, q):
    str = ""
    if time == 0.5:
        str = "%d\t \t \t \t \t \t \t " %q
    elif time == 1:
        str = " \t%d\t \t \t \t \t \t " %q
    elif time == 1.5:
        str = " \t \t%d\t \t \t \t \t " %q
    elif time == 2:
        str = " \t \t \t%d\t \t \t \t" %q
    elif time == 2.5:
        str = " \t \t \t \t%d\t \t \t " %q
    elif time == 3:
        str = " \t \t \t \t \t%q\t \t " %q
    elif time == 3.5:
        str = " \t \t \t \t \t \t%q\t " % q
    elif time == 4:
        str = " \t \t \t \t \t \t  \t%q" % q
    return str

def print(list):
    output = ""
    for row in list:
        output += "{}\t{}\n".format(row[0], row[1])
        output += "------------------------------------------------------------------------------------------\n"
    return output
