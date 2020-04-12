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
if(response.status_code == 200):

    # Get the list of tenants (domains) from the SMC
    url = 'https://' + SMC_HOST + '/sw-reporting/v1/tenants/'
    response = api_session.request("GET", url, verify=False)

    # If successfully able to get list of tenants (domains)
    if (response.status_code == 200):

        # Store the tenant (domain) ID as a variable to use later
        tenant_list = json.loads(response.content)["data"]
        SMC_TENANT_ID = tenant_list[0]["id"]

        # Print the SMC Tenant ID
        print("Tenant ID = {}".format(SMC_TENANT_ID))


    # If unable to fetch list of tenants (domains)
    else:
        print("An error has ocurred, while fetching tenants (domains), with the following code {}".format(response.status_code))

    uri = 'https://' + SMC_HOST + '/token'
    response = api_session.delete(uri, timeout=30, verify=False)

# If the login was unsuccessful
else:
        print("An error has ocurred, while logging in, with the following code {}".format(response.status_code))


