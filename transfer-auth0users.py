#! python3
import json
import http.client
import re
import urllib

    ## Written by Timothy Hutz; timothyhutz@gmail.com or timothy.hutz@thinktank.net
#global varaibles
_qa_auth0_connection = None
_qa_auth0_client_id = None
_qa_auth0_client_secret = None
_qa_auth0_db = None
_qa_auth0_api = None
_prod_auth0_connection = None
_prod_auth0_db = None
_prod_auth0_client_id = None
_prod_auth0_client_secret = None
_prod_auth0_api = None

## Getting token from auth0 qa and prod.
_qa_auth0_datatoken = None
while _qa_auth0_datatoken is None:
    conn = http.client.HTTPSConnection("%s" % _qa_auth0_connection)
    payload = "{\"client_id\":\"%s\",\"client_secret\":\"%s\",\"audience\":\"%s\",\"grant_type\":\"client_credentials\"}" % (_qa_auth0_client_id, _qa_auth0_client_secret, _qa_auth0_api)
    headers = { 'content-type': "application/json" }
    conn.request("POST", "/oauth/token", payload, headers)
    res = conn.getresponse()
    _qa_auth0_datatoken = res.read()
    _qa_auth0_datatoken_load = json.loads(_qa_auth0_datatoken)

_prod_auth0_datatoken = None
while _prod_auth0_datatoken is None:
    conn = http.client.HTTPSConnection("%s" % _prod_auth0_connection)
    payload = "{\"client_id\":\"%s\",\"client_secret\":\"%s\",\"audience\":\"%s\",\"grant_type\":\"client_credentials\"}" % (_prod_auth0_client_id, _prod_auth0_client_secret, _prod_auth0_api)
    headers = { 'content-type': "application/json" }
    conn.request("POST", "/oauth/token", payload, headers)
    res = conn.getresponse()
    _prod_auth0_datatoken = res.read()
    _prod_auth0_datatoken_load = json.loads(_prod_auth0_datatoken)

## finding user in qa then pulling full qa data, insert data into prod
def qa_userid_find(pagenum = int(0)):
    conn = http.client.HTTPSConnection("%s" % _qa_auth0_connection)
    payload = ""
    headers = { 'Authorization': "{token_type} {access_token}".format(token_type = _qa_auth0_datatoken_load['token_type'], access_token = _qa_auth0_datatoken_load['access_token']) }
    conn.request("GET", "/api/v2/users?per_page=1&page={pagenum}&connection={database}&fields=user_id".format(pagenum = pagenum, database = _qa_auth0_db), payload, headers)
    res = conn.getresponse()
    data = res.read()
    qa_auth0_userid = json.loads(data)
    return(qa_auth0_userid)

def qa_user_pull_full_data(user_id):
    conn = http.client.HTTPSConnection("%s" % _qa_auth0_connection)
    payload = ""
    headers = { 'Authorization': "{token_type} {access_token}".format(token_type = _qa_auth0_datatoken_load['token_type'], access_token = _qa_auth0_datatoken_load['access_token']) }
    conn.request("GET", '/api/v2/users/{id}'.format(id = user_id), payload, headers)
    res = conn.getresponse()
    data = res.read()
    return(data)

def prod_loaduser(email, user_metadata):
    conn = http.client.HTTPSConnection("{connection}".format(connection = _prod_auth0_connection))
    payload = "{\"connection\":\"%s\",\"email\":\"%s\",\"password\":\"<set_temp_passwd>\",\"user_metadata\":%s,\"email_verified\":true,\"verify_email\":false}" % (_prod_auth0_db, email, user_metadata)
    headers = { 'Authorization': "{token_type} {access_token}".format(token_type = _prod_auth0_datatoken_load['token_type'], access_token = _prod_auth0_datatoken_load['access_token']), "Content-Type": "application/json" }
    conn.request("POST", "/api/v2/users", payload, headers)
    res = conn.getresponse()
    data = res.read()
    return(data)

## Iteriator with parsed data.
pagenum = int(-1)
while pagenum is not -2:
    pagenum += int(1)
    qa_userid = str(qa_userid_find(pagenum))
    if re.match('\[\]', qa_userid):
        print("finished User ID search.")
        break
    else:
        ## For intail user load def from qa into prod
        qa_userid_cleanjson = re.sub(r'[\[\]]', '', qa_userid, 0, re.IGNORECASE)
        qa_userid_cleanjson = re.sub(r'[\']', '\"', qa_userid_cleanjson, 0, re.IGNORECASE)
        qa_userid_loadjson = json.loads(qa_userid_cleanjson)
        qa_userid_urlencode = urllib.parse.quote(qa_userid_loadjson['user_id'])
        qa_userid_fulldata_object = qa_user_pull_full_data(user_id = '{id}'.format(id = qa_userid_urlencode))
        prod_clean_insert_string = str(qa_userid_fulldata_object)
        prod_clean_remove_htmlbody = re.sub(r'^(b\')', '', prod_clean_insert_string, 0, re.IGNORECASE)
        prod_clean_remove_htmlbody = re.sub(r'(\')$', '', prod_clean_remove_htmlbody, 0, re.IGNORECASE)
        prod_data_jsonload = json.loads(prod_clean_remove_htmlbody)
        try:
            prod_data_user_metadata = {}
            prod_data_user_metadata_A = dict(prod_data_jsonload['user_metadata'])
            prod_data_user_metadata_B = dict({ "nickname": "%s" % (prod_data_jsonload['nickname']), 'name': '%s' % (prod_data_jsonload['name']) })
            prod_data_user_metadata = json.dumps({**prod_data_user_metadata_A, **prod_data_user_metadata_B})
            print(prod_data_user_metadata)
        except Exception:
            print('User Has no MetaData quried')
            prod_data_user_metadata = json.loads(json.dumps('{ "nickname": "%s", "name": "%s" }'  % (prod_data_jsonload['nickname'], prod_data_jsonload['name'])))

        print(prod_loaduser(user_metadata=prod_data_user_metadata, email=prod_data_jsonload['email']))
