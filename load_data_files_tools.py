__author__ = 'cmantas'

import urllib, urllib2, json, re, random

users_file = "data_files/users.json"
application_description_file = 'data_files/application_description.json'

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
    return json.loads(response)['id']

def load_application(user_id):
    """
    loads the applications and their modules from the applications file,
    injects in their JSON representation the information about the user ID and
    sends the 'addApplication' request
    @return:
    """
    url = "http://localhost:8084/celar_server/deployment/describeApplication"
    application_string = open(application_description_file, 'r').read()
    app = json.loads(application_string)
    #inject the user id of the app
    app['application']['USER_id'] = str(user_id)
    #put the json representation of the app in the HTTP "application" parameter
    application_string=json.dumps(app)
    args = {"application": application_string}
    response = get_REST_response(url, args)
    print"============== 'describeApplication' HTTP Responce ======================="
    print "content: " + response
    #recover the appId
    app_json_responce = json.loads(response)
    app_id = app_json_responce['id']
    return app_id





