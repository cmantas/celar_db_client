__author__ = 'cmantas'
import urllib2, json, MySQLdb
from DBTools import *
from kamaki.clients import ClientError

from kamaki.clients.astakos import AstakosClient
from kamaki.clients.cyclades import CycladesClient
#http://www.synnefo.org/docs/kamaki/latest/developers/code.html#the-client-api-ref
from sys import stderr
from os.path import abspath,exists
from os import mkdir
from base64 import b64encode


AUTHENTICATION_URL="https://accounts.okeanos.grnet.gr/identity/v2.0"
TOKEN="eESj-pRbtTCzh0o182b0JWhHRWlSYt6S-LpDp7WIZKA"

synnefo_user = AstakosClient(AUTHENTICATION_URL, TOKEN)

cyclades_endpoints = synnefo_user.get_service_endpoints('compute')
CYCLADES_URL = cyclades_endpoints['publicURL']
cyclades_client = CycladesClient(CYCLADES_URL, TOKEN)

# connect to db
db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="", db="celar_db")
cursor = db.cursor()

#get the max IDs for the tables
resources_table_id =get_table_max_id("PROVIDED_RESOURCE")
specs_table_id = get_table_max_id("SPECS")
if specs_table_id is None: specs_table_id=0
if resources_table_id is None:
    resources_table_id=0
resources_table_id+=1
#insert into  PROVIDED_RESOURCE table
cursor.execute("INSERT INTO PROVIDED_RESOURCE VALUES (%d, 'VM', '%s')" % (resources_table_id, "VM"))
#iterage through the flavors, get and store their specs
for flav in cyclades_client.list_flavors()[:5]:
    flav_id = flav['id']
    details=  cyclades_client.get_flavor_details(flav_id)
    ram=details['ram']; cores=details['vcpus']; disk=details['disk']; name = details['name'];
    #genarate a spec description dict and json
    spec_description={"flavor_id": flav_id, "ram": ram, "cores": cores, "disk": disk, "name": name}
    json_spec_description=json.dumps(spec_description)
    # execute SQL select statement
    specs_table_id+=1
    #insert into SPEC Description table
    cursor.execute("""INSERT INTO SPECS VALUES (%d, %d, '%s' ); """ %
                    (specs_table_id, resources_table_id, json_spec_description))

#commit insertions
db.commit()

#select all provided resources
cursor.execute("SELECT * FROM PROVIDED_RESOURCE")


# get the number of rows in the resultset
numrows = int(cursor.rowcount)
# get and display one row at a time.
for x in range(0,numrows):
    row = cursor.fetchone()
    print row

print "-------------------- SPECS ------------------------"

#select all provided resources
cursor.execute("SELECT * FROM SPECS")

# commit your changes
db.commit()

# get the number of rows in the resultset
numrows = int(cursor.rowcount)
# get and display one row at a time.
for x in range(0,numrows):
    row = cursor.fetchone()
    json_string= row[2]
    print json_string
    descr=json.loads(json_string)
