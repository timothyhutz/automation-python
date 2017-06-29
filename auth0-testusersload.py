#! python

import httplib
import json

    ### Written by Timothy Hutz; timothyhutz@gmail.com

_user = "user."
_connection = httplib.HTTPSConnection("None.auth0.com")
_auth0_clientid = "None"
_user_password = "None"
_connection_db = "None"

    ## Signs users up ...
for _u_int in range(1000):
    _post_headers = {'Content-Type': "application/json"}
    _user_email = _user+str(_u_int)+str('@email.com')
    _body_postdata = { 'client_id': _auth0_clientid, 'email': _user_email, 'password': _user_password, 'connection': _connection_db}
    _body_postdata_json = json.dumps(_body_postdata, sort_keys=True, indent=False)
    _connection.request('POST', "/dbconnections/signup", _body_postdata_json, _post_headers)
    _connection_response = _connection.getresponse()
    print _connection_response.read(), _connection_response.status, _connection_response.reason
    print _user_email
