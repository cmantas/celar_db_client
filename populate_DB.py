__author__ = 'cmantas'

from load_data_files_tools import *

#============ showoff of the get_spec_id_for_vm function
#find the SPECS_id of for a vm with the specified cores/ram/disk
cores = 1; ram = 1024; disk = 40;
print 'the RESOURCE_id for the VM with cores=%d, RAM=%d, disk=%d is: %d' % (cores, ram, disk, get_resource_id_for_vm(cores, ram, disk))

user_id = load_user()
print "added user id: %d" % user_id

application_id = load_application(user_id)
print "added application id: %d" % application_id

deploy_application(application_id)



