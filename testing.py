__author__ = 'cmantas'

import MySQLdb


# connect
db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="", db="celar_db")

cursor = db.cursor()

# execute SQL select statement
cursor.execute("SELECT MAX(id) FROM PROVIDED_RESOURCE")

# commit your changes
db.commit()

# get the number of rows in the resultset
numrows = int(cursor.rowcount)

# get and display one row at a time.
for x in range(0,numrows):
    row = cursor.fetchone()
    print row[0]