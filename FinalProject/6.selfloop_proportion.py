import pymysql
import pymysql.cursors
import matplotlib.pyplot as plt
import numpy as np
import math
import pickle

connection = pymysql.connect(host='localhost',
                             user='citation',
                             password='password',
                             db='citation',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

cursor = connection.cursor()

sql = "select * from journal_edges where edge_from=edge_to order by weight desc"

cursor.execute(sql)
rows = cursor.fetchall()
selfloops = []
sums = []
for row in rows:
    journal_id = str(row['edge_from'])
    selfloop = int(row['weight'])
    sql = "select sum(weight) as s from journal_edges where edge_from="+journal_id+" or edge_to="+journal_id
    cursor.execute(sql)
    row1 = cursor.fetchone()
    selfloops.append(selfloop)
    sums.append(int(row1['s']))
    print(selfloop, " in ", row1['s'])

selfloops = np.array(selfloops)
sums = np.array(sums)

I = selfloops / sums

print(I)