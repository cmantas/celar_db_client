__author__ = 'cmantas'

from load_data_files_tools import *

user_id = load_user()

print "added user id: "+ str(user_id)

application_id = load_application(user_id)

print "added application id: " + str(application_id)


#create_deployment(application_id)