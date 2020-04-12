#!/usr/bin/env python
import requests
import json
import datetime, time
try:
    requests.packages.urllib3.disable_warnings()
except:
    pass


# Enter all authentication info
SMC_USER = "admin"
SMC_PASSWORD = "C1sco12345"
SMC_HOST = "10.10.20.60"
SMC_TENANT_ID = "132"
MALICIOUS_IP = "10.10.20.20"

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

    # Set the URL for the query to POST the filter and initiate the search
    url = 'https://' + SMC_HOST + '/sw-reporting/v1/tenants/' + SMC_TENANT_ID + '/security-events/queries'

    # Set the timestamps for the filters, in the correct format, for last 60 minutes
    end_datetime = datetime.datetime.utcnow()
    start_datetime = end_datetime - datetime.timedelta(minutes=60)
    end_timestamp = end_datetime.strftime('%Y-%m-%dT%H:%M:%SZ')
    start_timestamp = start_datetime.strftime('%Y-%m-%dT%H:%M:%SZ')

    # Set the filter with the request data
    request_data = {
        "timeRange": {
            "from": start_timestamp,
            "to": end_timestamp
        },
        "hosts": [
            {
                "ipAddress": MALICIOUS_IP,
                "type": "source"
            }
        ],
    }

    # Perform the query to initiate the search
    request_headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    response = api_session.request("POST", url, verify=False, data=json.dumps(request_data), headers=request_headers)

    # If successfully able to initiate search, grab the search details
    if (response.status_code == 200):
        print("Generating results. Please wait...\n")
        search = json.loads(response.content)["data"]["searchJob"]
        search_id = search["id"]

        # Set the URL to check the search status
        url = 'https://' + SMC_HOST + '/sw-reporting/v1/tenants/' + SMC_TENANT_ID + '/security-events/queries/' + search_id

        # While search status is not complete, check the status every second
        while search["percentComplete"] != 100.0:
            response = api_session.request("GET", url, verify=False)
            search = json.loads(response.content)["data"]
            time.sleep(1)

        # Set the URL to check the search results and get them
        url = 'https://' + SMC_HOST + '/sw-reporting/v1/tenants/' + SMC_TENANT_ID + '/security-events/results/' + search_id
        response = api_session.request("GET", url, verify=False)
        results = json.loads(response.content)["data"]["results"]

        # Loop through the results and print each row in a new line
        for row in results:
            print(row)

    # If unable to update the IPs for a given tag (host group)
    else:
        print("An error has ocurred, while getting security events, with the following code {}".format(response.status_code))

    uri = 'https://' + SMC_HOST + '/token'
    response = api_session.delete(uri, timeout=30, verify=False)

# If the login was unsuccessful
else:
        print("An error has ocurred, while logging in, with the following code {}".format(response.status_code))


