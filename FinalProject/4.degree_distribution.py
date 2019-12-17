import pymysql
import pymysql.cursors
import matplotlib.pyplot as plt
import numpy as np
import math

connection = pymysql.connect(host='localhost',
                             user='citation',
                             password='password',
                             db='citation',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

cursor = connection.cursor()

sqls = [
    "select sum(weight) as total_weight, edge_to from journal_edges group by edge_to",
    "select sum(weight) as total_weight, edge_to from journal_edges where edge_from<>edge_to group by edge_to",
    "select sum(weight) as total_weight, edge_from from journal_edges group by edge_from",
    "select sum(weight) as total_weight, edge_from from journal_edges where edge_from<>edge_to group by edge_from",
    ]
titles = [
    "in-degree distribution w/ self-loops",
    "in-degree distribution w/o self-loops",
    "out-degree distribution w/ self-loops",
    "out-degree distribution w/o self-loops",    
]
subplots = []
fig, axes = plt.subplots(2,2, figsize=(10,6))
for i in range(4):
    print(math.floor(i/2), ",", i%2)
    ax = axes[math.floor(i/2), i%2]
    try:
        sql = sqls[i]
        cursor.execute(sql)
        rows = cursor.fetchall()
        total_weight = []
        for row in rows:
            total_weight.append(int(row['total_weight']))
    except pymysql.err.MySQLError as e:
        print("When processing select")
        print('Got error {!r}, errno is {}'.format(e, e.args[0]))


    logbins = [1.00000000e+00,1.51906381e+00,2.30755487e+00,3.50532310e+00,5.32480947e+00,8.08872538e+00,1.22872900e+01,1.86651776e+01,2.83535959e+01,4.30709216e+01,6.54274783e+01,9.93885148e+01,1.50977496e+02,2.29344451e+02,3.48388857e+02,5.29224905e+02,8.03926402e+02,1.22121551e+03,1.85510428e+03,2.81802179e+03,4.28075492e+03,6.50273990e+03,9.87807686e+03,1.50054291e+04,2.27942044e+04,3.46258510e+04,5.25988773e+04,7.99010511e+04,1.21374795e+05,1.84376059e+05,2.80079000e+05]
    ax.hist(total_weight, bins=logbins)
    ax.set_title(titles[i])
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("Total Weights")
    ax.set_ylabel("Number of Journals")
plt.tight_layout()
plt.show()
