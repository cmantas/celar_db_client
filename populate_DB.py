__author__ = 'cmantas'

from load_data_files_tools import *

# get the SPEC id for a VM resource, given its core count, RAM, and disk
cores = 1; ram = 1024; disk = 40;
# print 'the RESOURCE_id for the VM with cores=%d, RAM=%d, disk=%d is: %d' % \
#       (cores, ram, disk, get_resource_id_for_vm(cores, ram, disk))


#get the user configuration from a file, add in the DB and get the id of the added user
user_id = load_user()
print "added user id: %d" % user_id


# #load the application configuration from a file and add it in the DB, with a given user id as its "owner"
# #from the previous step
# application_id = load_application(user_id)
# print "added application id: " + application_id
#
#
# #load the deployement configuration from a file and add it in the DB, with a given application id
# deployment_id = deploy_application(application_id)
#
#
# #get the deployment for the specified deployment id (to see if everything worked
# get_deployment_configuration(deployment_id)
#


