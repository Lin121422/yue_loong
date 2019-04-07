import math
import sqlite3
from django.shortcuts import render
# 經濟訂購量


# d為年需求、s為訂購成本、h為年持有成本


def epq(name1):
    conn = sqlite3.connect('FinalPro.db')
    cursor1 = conn.execute("select 年需求 from main.Product where Product_Name= '%s'" % name1)
    cursor2 = conn.execute("select 訂購成本 from main.Product where Product_Name='%s'" % name1)
    cursor3 = conn.execute("select 年持有成本 from main.Product where Product_Name='%s'" % name1)
    cursor4 = conn.execute("select 日生產率 from main.Product where Product_Name='%s'" % name1)
    cursor5 = conn.execute("select 日使用率 from main.Product where Product_Name='%s'" % name1)
    d=0
    s=0
    h=0
    p=0
    u=0
    for r in cursor1:
        d=int(r[0])
    for r in cursor2:
        s=int(r[0])
    for r in cursor3:
        h=int(r[0])
    for r in cursor4:
        p=int(r[0])
    for r in cursor5:
        u=int(r[0])
    q = math.sqrt(2*d*s/h)*math.sqrt(p/(p-u))
    return q


# 最高存貨水準
def i_max(name2):
    conn = sqlite3.connect('FinalPro.db')
    cursor4 = conn.execute("select 日生產率 from main.Product where Product_Name='%s'" % name2)
    cursor5 = conn.execute("select 日使用率 from main.Product where Product_Name='%s'" % name2)
    imax = epq(name2)/cursor4*(cursor4-cursor5)
    return imax


def eoq(name1):
    conn = sqlite3.connect('FinalPro.db')
    cursor1 = conn.execute("select 年需求 from main.Product where Product_Name= '%s'" % name1)
    cursor2 = conn.execute("select 訂購成本 from main.Product where Product_Name='%s'" % name1)
    cursor3 = conn.execute("select 年持有成本 from main.Product where Product_Name='%s'" % name1)
    d = 0
    s = 0
    h = 0
    for r in cursor1:
        d = int(r[0])
    for r in cursor2:
        s = int(r[0])
    for r in cursor3:
        h = int(r[0])
    q = math.sqrt(2 * d * s / h)
    return round(q)

# 平均存貨水準
def i_avg(name3):
    iavg = i_max(name3)/2
    return iavg
