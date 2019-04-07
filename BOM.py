import sqlite3

'''
    物料清單
    output : 階層、名稱、數量
'''
def bom():
    bomtable = print(carBom(1)) + "\n" + print(carBom(2))
    return bomtable

def carBom(id):
    conn = sqlite3.connect('FinalPro.db')
    if id == 1:
        name = "Car 1"
    elif id == 2:
        name = "Car 2"
    cartable = []
    cartable.append(["階層", "名稱", "數量"])
    cartable.append([0, name, id])
    cursor = conn.execute("select Part_ID, Part_Name, Part_Included from main.Part where Part_ID like '_{}%'".format(id))
    for row in cursor:
        layer = row[0][2]
        part = [int(layer), row[1], int(row[2])]
        cartable.append(part)
    conn.close()
    return cartable

def print(list):
    output = ""
    for part in list:
        output += "{:4}\t{:4}\t{:4}\n".format(part[0], part[1], part[2])
        output += "------------------------------\n"
    return output
