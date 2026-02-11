#!/usr/bin/env python
'''
Example functions to interact with IOS XE Livetools API using RESTCONF.

Copyright (c) 2026 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
'''

__copyright__ = "Copyright (c) 2026 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"
__author__ = "Juulia Santala"
__email__ = "jusantal@cisco.com"

import requests
import urllib3

urllib3.disable_warnings()

HEADERS = {
    'Content-Type': 'application/yang-data+json',
    'Accept': 'application/yang-data+json',
}

def ping_action(host:str, username:str, password:str, target_ip:str)->int:

    base_url = f"https://{host}:443/restconf"
    action_url = f"{base_url}/operations/Cisco-IOS-XE-livetools-actions-rpc:ip-ping-action"
    body = {
        "count": 3,
        "host-ip":target_ip
    }
    auth = (username, password)
    response = requests.post(action_url, headers=HEADERS, json=body, auth=auth, verify=False)
    print(f"Request status code: {response.status_code}")
    
    if response.ok:
        return response.json()["Cisco-IOS-XE-livetools-actions-rpc:output"]["job-id"]
    else:
        return None

def traceroute_action(host:str, username:str, password:str, target_ip:str="10.128.128.5")->int:
    base_url = f"https://{host}:443/restconf"
    action_url = f"{base_url}/operations/Cisco-IOS-XE-livetools-actions-rpc:ip-tracert-action"
    body = {
        "host-ip":target_ip
    }
    auth = (username, password)

    response = requests.post(action_url, headers=HEADERS, json=body, auth=auth, verify=False)
    print(f"Request status code: {response.status_code}")

    if response.ok:
        return response.json()["Cisco-IOS-XE-livetools-actions-rpc:output"]["job-id"]
    else:
        return None

def traceroute_results(host:str, username:str, password:str, job_id:int=None):

    base_url = f"https://{host}:443/restconf"
    result_url = f"{base_url}/data/Cisco-IOS-XE-livetools-oper:livetools-oper-data/tracert-result"
    auth = (username, password)

    response = requests.get(f"{result_url}{f'={job_id}' if job_id else ''}", headers=HEADERS, auth=auth, verify=False)
    if response.ok:
        return response.json().get("Cisco-IOS-XE-livetools-oper:tracert-result")
    else:
        return None

def ping_results(host:str, username:str, password:str, job_id:int=None)->list:

    base_url = f"https://{host}:443/restconf"
    result_url = f"{base_url}/data/Cisco-IOS-XE-livetools-oper:livetools-oper-data/ip-ping-result"
    auth = (username, password)

    response = requests.get(f"{result_url}{f'={job_id}' if job_id else ''}", headers=HEADERS, auth=auth, verify=False)
    if response.ok:
        return response.json().get("Cisco-IOS-XE-livetools-oper:ip-ping-result")
    else:
        return None