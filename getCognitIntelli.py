#!/usr/bin/env python

import requests
import json

try:
    requests.packages.urllib3.disable_warnings()
except:
    pass

# Enter all authentication info
SMC_USER = "admin"
SMC_PASSWORD = "C1sco12345"
SMC_HOST = "10.10.20.60"
MALICIOUS_IP = "10.10.20.2"

# Set the URL for SMC login
url = "https://" + SMC_HOST + "/token/v2/authenticate"

# Let's create the login request data
login_request_data = {
    "username": SMC_USER,
    "password": SMC_PASSWORD
}

# Initialize the Requests session
api_session = requests.Session()

# Perform the POST request to login
response = api_session.request("POST", url, verify=False, data=login_request_data)

# If the login was successful
if (response.status_code == 200):

    # Get the list of Cognitive Intelligence incidents from the SMC
    url = 'https://' + SMC_HOST + '/sw-reporting/v2/tenants/0/incidents?ipAddress=' + MALICIOUS_IP
#    url = 'https://' + SMC_HOST + '/sw-reporting/v2/tenants/0/incidents'

    response = api_session.request("GET", url, verify=False)

    # If successfully able to get list of Cognitive Intelligence incidents
    if (response.status_code == 200):

        # Loop through the list and print Cognitive Intelligence incident
        # print(json.loads(response.content))  //Test if the CTA service in on!
        # {'errors': [{'status': 'cta_not_enabled', 'description': 'No data available. CTA is not enabled on SMC'}]}
        incidents = json.loads(response.content)["data"]
        for incident in incidents:
            print(incident)

    # If unable to fetch list of Cognitive Intelligence incidents
    else:
        print(
            "An error has ocurred, while fetching Cognitive Intelligence incidents, with the following code {}".format(
                response.status_code))

    uri = 'https://' + SMC_HOST + '/token'
    response = api_session.delete(uri, timeout=30, verify=False)

# If the login was unsuccessful
else:
    print("An error has ocurred, while logging in, with the following code {}".format(response.status_code))
