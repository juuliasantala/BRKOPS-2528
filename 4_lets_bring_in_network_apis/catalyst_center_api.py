#!/usr/bin/env python
'''
Retrieve interface configuration from Catalyst Center for the selected device.

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

host = "198.18.129.100"
username = "admin"
password = "C1sco12345"
device_uuid = "46e039eb-2f9b-4832-9abe-68a22044942f"

# Get auth token
url = f"https://{host}/dna/system/api/v1/auth/token"
response = requests.post(url, auth=(username, password), verify=False)
token = response.json()["Token"]

# Get device interfaces
url = f"https://{host}/dna/intent/api/v1/interface/network-device/{device_uuid}"
interfaces = requests.get(url,headers={"x-auth-token":token}, verify=False)

interfaces = interfaces.json()["response"]

import pprint
pprint.pprint(interfaces)
