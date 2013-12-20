__author__ = 'cmantas'
import MySQLdb


# connect
db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="", db="celar_db")

cursor = db.cursor()

def get_table_max_id(table_name):
    # execute SQL select statement
    cursor.execute("SELECT MAX(id) FROM %s" % table_name)
    # commit your changes
    db.commit()
    numrows = int(cursor.rowcount)
    for x in range(0,numrows):
        row = cursor.fetchone()
        return row[0]