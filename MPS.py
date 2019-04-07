# master production schedule(MPS, 主排程)
from django.shortcuts import render
from operations.EOQ_EPQ import epq
import sqlite3
import prettytable as pt


# initial_inv代表期初存貨、predict為預測值(為list)、promised_order為已承諾顧客訂單(為list)
def mps(year, quarter):
    conn = sqlite3.connect('FinalPro.db')
    if quarter == '1':
        month1 = '1'
        month2 = '2'
        month3 = '3'
    elif quarter == '2':
        month1 = '4'
        month2 = '5'
        month3 = '6'
    elif quarter == '3':
        month1 = '7'
        month2 = '8'
        month3 = '9'
    elif quarter == '4':
        month1 = '10'
        month2 = '11'
        month3 = '12'
    else:
        print("一年只有四季！")

    # 預測 car1_predict,  car2_predict
    cursor = conn.execute("select 年需求 from main.Product")
    predict = []
    for row in cursor:
        row=int(row[0])
        row=round(row/12)
        predict.append(row)
    car1_predict = [predict[0]]*3
    car2_predict = [predict[1]]*3

    # 已承諾訂單  promised_order

    # cursor1 = conn.execute("select Order_ID from main.Place where Order_Date=_____month1")
    # cursor2 = conn.execute("select Order_ID from main.Place where Order_Date=_____month2")
    # cursor3 = conn.execute("select Order_ID from main.Place where Order_Date=_____month3")

    cursor4 = conn.execute("select Shipping_Quantities from main.OrderHas where Order_ID IN (select Order_ID from main.Place where Order_Due_Date like '{0}_{1}%')".format(year, month1))
    cursor5 = conn.execute("select Shipping_Quantities from main.OrderHas where Order_ID IN (select Order_ID from main.Place where Order_Due_Date like '{0}_{1}%')".format(year, month2))
    cursor6 = conn.execute("select Shipping_Quantities from main.OrderHas where Order_ID IN (select Order_ID from main.Place where Order_Due_Date like '{0}_{1}%')".format(year, month3))
    promised_order = []
    order1 = 0
    order2 = 0
    order3 = 0
    for row in cursor4:
        row=int(row[0])
        order1 += row
    promised_order.append(order1)
    for row in cursor5:
        row=int(row[0])
        order2 += row
    promised_order.append(order2)
    for row in cursor6:
        row=int(row[0])
        order3 += row
    promised_order.append(order3)

    # 期初存貨  init_inv
    cursor7 = conn.execute("select Quantity_In_Hand from main.Product")
    init_inv = []
    for row in cursor7:
        init_inv.append(int(row[0]))

    # 主排程  input: car1_predict, car2_predict, promised_order, init_inv     output： cur_inv,  mps_list, cur_inv2,  mps_list2
    # car1
    cur_inv=[0]*len(car1_predict)
    mps_list=[0]*len(car1_predict)
    for i in range(0, len(car1_predict)):
        if i == 0:
            cur_inv[i] = round(init_inv[0]-max(car1_predict[i], promised_order[i]))
            if cur_inv[i] <= 10:  # 10為安全存量
                mps_list[i] = round(epq("Car 1"))
                cur_inv[i] = round(cur_inv[i]+mps_list[i])
            else:
                mps_list[i]=0
        else:
            cur_inv[i] = round(cur_inv[i-1] - max(car1_predict[i], promised_order[i]))
            if cur_inv[i] <= 10:   # 10為安全存量
                mps_list[i] = round(epq("Car 1"))
                cur_inv[i] = round(cur_inv[i]+mps_list[i])
            else:
                mps_list[i] = 0

    # car2
    cur_inv2 = [0] * len(car2_predict)
    mps_list2 = [0] * len(car2_predict)
    for i in range(0, len(car2_predict)):
        if i == 0:
            cur_inv2[i] = round(init_inv[1] - max(car2_predict[i], promised_order[i]))
            if cur_inv2[i] <= 10:  # 10為安全存量
                mps_list2[i] = round(epq("Car 2"))
                cur_inv2[i] = round(cur_inv2[i] + mps_list2[i])
            else:
                mps_list2[i] = 0
        else:
            cur_inv2[i] = round(cur_inv2[i - 1] - max(car2_predict[i], promised_order[i]))
            if cur_inv2[i] <= 10:  # 10為安全存量
                mps_list2[i] = round(epq("Car 2"))
                cur_inv2[i] = round(cur_inv2[i] + mps_list2[i])
            else:
                mps_list2[i] = 0

    # 表格方式呈現
    table1 = pt.PrettyTable()
    table1.field_names = ["Car 1", "主", "排", "程"]
    table1.add_row(["月份", "{0}".format(month1), "{0}".format(month2), "{0}".format(month3)])
    table1.add_row(["現有庫存量" ,  "{0}".format(cur_inv[0]), "{0}".format(cur_inv[1]), "{0}".format(cur_inv[2])])
    table1.add_row(["MPS",  "{0}".format(mps_list[0]), "{0}".format(mps_list[1]), "{0}".format(mps_list[2])])

    table2 = pt.PrettyTable()
    table2.field_names = ["Car 2", "主", "排", "程"]
    table2.add_row(["月份",  "{0}".format(month1), "{0}".format(month2), "{0}".format(month3)])
    table2.add_row(["現有庫存量", "{0}".format(cur_inv2[0]), "{0}".format(cur_inv2[1]), "{0}".format(cur_inv2[2])])
    table2.add_row(["MPS", "{0}".format(mps_list2[0]), "{0}".format(mps_list2[1]), "{0}".format(mps_list2[2])])

    return mps_list, mps_list2, table1, table2

