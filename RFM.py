import sqlite3
import math
import prettytable as pt

# output: rfmList(有顧客姓名、RFM小組編號)
def rfm():
    conn = sqlite3.connect("FinalPro.db")

    # recency
    cursor1 = conn.execute("select Customer_ID, Order_Due_Date from main.Place ORDER BY Order_Due_Date ASC ")
    recency = []
    for row in cursor1:
        if list(row) in recency:
            continue
        else:
            recency.append(list(row))
    n1 = math.floor(len(recency)/5)
    clear_R = list(recency[i:i + n1] for i in range(0,len(recency),n1))
    if len(clear_R) > 5:
        for i in range(0, len(clear_R[5])):
            clear_R[4].append(clear_R[5][i])
        clear_R.pop()
    # 賦予R值
    for i in range(0,5):
        for d in range(0, len(clear_R[i])):
            clear_R[i][d].append(i+1)



    print(clear_R)

    # 寫入資料庫(UPDATE)
    for g in range(len(clear_R)):
        for h in range(len(clear_R[g])):
            conn.execute("update main.Customer \
                          set Recency = {0} \
                          where Customer_ID = '{1}' ".format(clear_R[g][h][2], clear_R[g][h][0]))
            conn.commit()


    # frequency
    cursor2 = conn.execute("select Customer_ID, SUM(Place_Amount/Place_Amount) from main.Place \
                           group by Customer_ID \
                           order by SUM(Place_Amount/Place_Amount) DESC")
    ordered_frequency = []
    for row in cursor2:
        frequency = list(row)
        ordered_frequency.append(frequency)
    n2 = math.floor(len(ordered_frequency)/5)
    clear_F = list(ordered_frequency[i:i + n2] for i in range(0, len(ordered_frequency), n2))
    if len(clear_F) > 5:
        for i in range(0, len(clear_F[5])):
            clear_F[4].append(clear_F[5][i])
        clear_F.pop()
    # 賦予F值
    for i in range(0,5):
        for d in range(0, len(clear_F[i])):
            clear_F[i][d].append(i+1)


    # 寫入資料庫(UPDATE)
    for g in range(len(clear_F)):
        for h in range(len(clear_F[g])):
            conn.execute("update main.Customer \
                              set Frequency = {0} \
                              where Customer_ID= '{1}' ".format(clear_F[g][h][2], clear_F[g][h][0]))
            conn.commit()

    # monetary value
    cursor3 = conn.execute("select a1.Customer_ID, SUM(a2.Shipping_Quantities * a3.Product_Price) \
                           from main.Place as a1, main.OrderHas as a2, main.Product as a3 \
                            where a1.Order_ID=a2.Order_ID and a2.Product_ID=a3.Product_ID \
                            group by a1.Customer_ID")
    ordered_monetary = []
    for row in cursor3:
        value = list(row)
        ordered_monetary.append(value)
    n3 = math.floor(len(ordered_monetary)/5)
    clear_M = list(ordered_monetary[i:i + n3] for i in range(0, len(ordered_monetary), n3))
    if len(clear_M) > 5: # 超過五組
        for i in range(0, len(clear_M[5])):
            clear_M[4].append(clear_M[5][i])
    clear_M.pop()
    # 賦予M值
    for i in range(0,5):
        for d in range(0, len(clear_M[i])):
            clear_M[i][d].append(i+1)


    # 寫入資料庫(UPDATE)
    for g in range(len(clear_F)):
        for h in range(len(clear_F[g])):
            conn.execute("update main.Customer \
                          set Monetary = {0} \
                          where Customer_ID= '{1}' ".format(clear_F[g][h][2], clear_F[g][h][0]))
            conn.commit()

    # 使用RFM值
    cursor4 = conn.execute("select Customer_ID, Recency, Frequency, Monetary from main.Customer")
    rfmList = []
    for i in cursor4:
        rfmList.append(list(i))
    for d in range(len(rfmList)):
        rfmList[d].append(rfmList[d][1]*100 + rfmList[d][2]*10 + rfmList[d][3])

    # 寫入資料庫
    for j in range(len(rfmList)):
        conn.execute("update Customer set 小組編號= {0} where Customer_ID = '{1}'".format(rfmList[j][4], rfmList[j][0]))
        conn.commit()

    # 表格方式呈現
    cursor5 = conn.execute("select Customer_Name, 小組編號 from main.Customer")
    present = []
    for k in cursor5:
        present.append(list(k))
    table1 = pt.PrettyTable()
    table1.field_names = ["顧客姓名", "RFM小組編號"]
    for k in range(len(present)):
        table1.add_row(["{0}".format(present[k][0]), "{0}".format(present[k][1])])

    return table1


