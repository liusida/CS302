sql = """
select j_f.journal_name as Source, j_t.journal_name as Target, weight
from (
select * from journal_edges where edge_from in 
((select distinct edge_from from journal_edges where edge_to=50372074 and weight>500)
union
(select distinct edge_to from journal_edges where edge_from=50372074 and weight>500))
and edge_to in 
((select distinct edge_from from journal_edges where edge_to=50372074 and weight>500)
union
(select distinct edge_to from journal_edges where edge_from=50372074 and weight>500))
and weight>500 and edge_from<>edge_to
) t 
left join journals j_f on j_f.journal_id=t.edge_from
left join journals j_t on j_t.journal_id=t.edge_to
"""

filename = "citation_env.graphml"

sql = """
select j_f.journal_name as Source, j_t.journal_name as Target, weight from journal_edges 
left join journals j_f on j_f.journal_id=journal_edges.edge_from
left join journals j_t on j_t.journal_id=journal_edges.edge_to
where weight>1000 and edge_from<>edge_to
"""

filename = "whole_network.graphml"

import json
import pymysql
import pymysql.cursors
import sys
import networkx as nx

G = nx.DiGraph()
connection = pymysql.connect(host='localhost',
                             user='citation',
                             password='password',
                             db='citation',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

cursor = connection.cursor()

try:
    
    cursor.execute(sql)
    rows = cursor.fetchall()
    edges = []
    for row in rows:
        edges.append([row['Source'], row['Target'], row['weight']])
    G.add_weighted_edges_from(edges)
    print(G.number_of_nodes())

except pymysql.err.MySQLError as e:
    print("When processing select")
    print('Got error {!r}, errno is {}'.format(e, e.args[0]))    

# try:
#     sql = "SELECT * FROM journals"
#     cursor.execute(sql)
#     rows = cursor.fetchall()
#     for row in rows:
#         if G.has_node(row['journal_id']):
#             G.nodes[row['journal_id']]['title'] = row['journal_name']
# except pymysql.err.MySQLError as e:
#     print("When processing select")
#     print('Got error {!r}, errno is {}'.format(e, e.args[0]))    

nx.readwrite.graphml.write_graphml(G,filename)