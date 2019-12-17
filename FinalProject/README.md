# Source Code for Final Project Journal Citation Network

## Data Source

Please download the data zip file from (https://lfs.aminer.cn/misc/dblp.v11.zip).

## MySQL

Please use MySQL Community Server (Open Source) Ver 8.0.18 from (https://dev.mysql.com/downloads/mysql/), and install.

Then create a database called `citation` to receive the data and create a user called `citation` and password is `passwd` who can manage that database.

## Files

`1. write_into_mysql.py` reads from the downloaded file and extract critical data into MySQL.

`2. count_journal_edges.py` counts journal edges and create a table for journal edges.

`3. read_journal_network.py` creates a graphml file for Gephi to read.

`4. degree_distribution.py` plot degree distribution of the journal network.

`5. citation_env.py` create a graphml file of citation environment for Gephi to do visualization.

`6. selfloop_proportion.py` measures the self-loops and the introversion I.
 
