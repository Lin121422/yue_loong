import sqlite3
import random
import datetime


# 新增訂單  input：product_name,
def create(product_name, quantity, discount):
    conn = sqlite3.connect('FinalPro.db')
    # orderHas
    oid_list = []
    if product_name=='Car 1':
        a = conn.execute("select Order_ID from OrderHas")
        for i in a:
            oid_list.append(list(i))

        conn.execute("insert into OrderHas (Product_ID, Order_ID, Shipping_Quantities, Shipping_status) \
                      values ('PD0001', 'OD910100{0}', '{1}', '0 未出單' )".format(len(oid_list)+1, quantity))
        conn.commit()
    else:
        a = conn.execute("select Order_ID from OrderHas")
        for i in a:
            oid_list.append(list(i))

        conn.execute("insert into OrderHas (Product_ID, Order_ID, Shipping_Quantities, Shipping_status) \
                                 values ('PD0002', 'OD910100{0}', '{1}', '0 未出單' )".format(len(oid_list)+1, quantity))
        conn.commit()
    # deal with
    conn.execute("insert into DealWith (Sales_ID, Order_ID, Performance) \
                  values ('SA000000{0}', 'OD910100{1}', ' ')".format(random.randint(1,5), len(oid_list)+1))
    conn.commit()

    # BookOrder
    conn.execute("insert into BookOrder (Order_ID, Discount) \
                 values ('OD910100{0}', '{1}')".format(len(oid_list)+1, discount))
    conn.commit()

    # place
    today=datetime.date.today()
    conn.execute("insert into Place (Customer_ID, Order_ID, Place_Amount, Order_Due_Date) \
                 values ('AA0000000{0}', 'OD910100{1}', {2}, '{3}/{4}/{5}')".format(random.randint(1,9), len(oid_list)+1, quantity, today.year, today.month, today.day))
    conn.commit()

    # 輸出
    ans = conn.execute("select a1.Order_ID, a6.Customer_Name, a5.Product_Name, a2.discount, a1.Place_Amount, a1.Order_Due_Date, a3.Sales_ID \
                        from  Place as a1,BookOrder as a2, DealWith as a3, OrderHas as a4, Product as a5, Customer as a6 \
                       where a1.Order_ID = 'OD910100{0}' and a1.Order_ID=a2.Order_ID and a1.Order_ID=a3.Order_ID and  a1.Order_ID=a4.Order_ID and a4.Product_ID=a5.Product_ID and a1.Customer_ID=a6.Customer_ID".format(len(oid_list)+1))
    for i in ans:
        i = list(i)
        res = "成功輸入一筆訂單，其Order_ID為 {0}  消費者名字為{1} 產品名稱為{2} \n 折扣為{3}\n 訂購數量為{4}".format(i[0], i[1], i[2], i[3], i[4])
    conn.close()
    return res

# "成功輸入一筆訂單，其Order_ID為{0}".format('OD910100{0}'.format(len(oid_list)+1))   可加入作為output



