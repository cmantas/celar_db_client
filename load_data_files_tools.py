__author__ = 'cmantas'

import urllib, urllib2, json, re, random

users_file = "data_files/users.json"
application_description_file = 'data_files/application_description.json'
configuration_file= 'data_files/application_configuration.json'

def get_REST_response(url, args):
    data = urllib.urlencode(args)
    req = urllib2.Request(url, data)
    rsp = urllib2.urlopen(req)
    return rsp.read()


def load_user():
    """
    loads the users from the users file
    """
    url = 'http://localhost:8084/celar_server/deployment/addUser'
    users_string = open(users_file, 'r').read()
    args = {"user": users_string}
    response = get_REST_response(url, args)
    # print result
    print "======= 'AddUser' HTTP Responce ================="
    print response
    return int(response)

def load_application(user_id):
    """
    loads the applications and their modules from the applications file,
    injects in their JSON representation the information about the user ID and
    sends the 'addApplication' request
    @return:
    """
    url = "http://localhost:8084/celar_server/deployment/describe"
    application_string = open(application_description_file, 'r').read()
    app = json.loads(application_string)
    #inject the user id of the app
    app['application']['USER_id'] = str(user_id)
    #put the json representation of the app in the HTTP "application" parameter
    application_string=json.dumps(app)
    args = {"application": application_string}
    response = get_REST_response(url, args)
    print"============== 'describe' HTTP Responce ======================="
    print response
    #recover the appId
    app_id = int(response)
    return app_id


def deploy_application(app_id):
    """
    loads the resources that will be assigned to the deployment from the application configuration file,
    injects in their JSON representation the information about the app ID and
    sends the 'deploy' request
    @param app_id:
    @return:
    """
    url = "http://localhost:8084/celar_server/deployment/deploy"
    config_str = open(configuration_file, 'r').read()
    args = {"ApplicationId": app_id, 'deployment_configuration': config_str}
    response = get_REST_response(url, args)
    print('========================= "deploy" HTTP responce =================')
    print response
    deployment_id=int(response)
    return deployment_id

def get_deployment_configuration(deployment_id, timestamp="now"):
    """
    gets the current deployement configuration for the specified deployment id
    @param deployment_id:
    @return:
    """
    url = "http://localhost:8084/celar_server/deployment/getConfiguration"
    config_str = open(configuration_file, 'r').read()
    args = {"DeploymentId": deployment_id, 'timestamp': timestamp}
    response = get_REST_response(url, args)
    print('========================= "getConfiguration" HTTP responce =================')
    print response


def get_resource_id_for_vm(cores=1, ram=1024, disk=20):
    """
    loads from celar_db the specs of all VMs and searches in them for the id of the one
    that satisfies the required cores/ram/disk values
    @param cores: the number of cores of the desired vm
    @param ram: the RAM of the desired vm (MB)
    @param disk: the disk size of the desired vm (GB)
    @return: the SPEC_ID of the desired resource
    """
    url = "http://localhost:8084/celar_server/iaas/resources"
    config_str = open(configuration_file, 'r').read()
    args = {'type': 'VM'}
    response = get_REST_response(url, args)
    print('========================= "resources" HTTP responce =================')
    print response
    provided_resources = json.loads(response)['provided_resources']
    #from the provided resources find the one of type VM and keep the specs table
    for resource in provided_resources:
        if resource['type'] != 'VM':
            continue
        specs=resource['specs']
        for s in specs:
            description = json.loads(s['description'])
            try:
                spec_cores= description['cores']
                spec_ram= description['ram']
                spec_disk= description['disk']
                if spec_cores==cores and spec_ram==ram and spec_disk==disk:
                    return resource['id']
            except:
                continue
    return None