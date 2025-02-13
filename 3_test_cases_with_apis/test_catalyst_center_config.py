#!/usr/bin/env python
'''
Configuration validation ("Is it there?") to test port status by
executing a simple Catalyst Center API test.

Copyright (c) 2025 Cisco and/or its affiliates.
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

__copyright__ = "Copyright (c) 2025 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"
__author__ = "Juulia Santala"
__email__ = "jusantal@cisco.com"

from pyats import aetest
import requests

class InterfaceConfigTestcase(aetest.Testcase):

    @aetest.setup
    def get_cc_token(self, cat_creds, device_list):
        self.cat_url = cat_creds['url']
        url = f"https://{cat_creds['url']}/dna/system/api/v1/auth/token"

        try:
            auth = (cat_creds['username'], cat_creds['password'])
            response = requests.post(url, auth=auth, verify=False)
            self.token = response.json()["Token"]

        except Exception as err:
             self.fail(err)
             
        else:
            aetest.loop.mark(self.get_device_interface_details, device=device_list)


    @aetest.test
    def get_device_interface_details(self, steps, device):
        '''
        Retrieve interface configuration from Catalyst Center for the selected device
        '''
        with  steps.start(
            f" Retrieving interface details for: {device['name']}",
            continue_=True
        ) as step:

            try:
                url = f"https://{self.cat_url}/dna/intent/api/v1/interface/network-device/{device['uuid']}"
                interfaces = requests.get(url,headers={"x-auth-token":self.token}, verify=False)
                self.interfaces = interfaces.json()["response"]
            except Exception as err:
                step.failed(err)
            else:
                step.passed()

    @aetest.test
    def test_interface_status(self, steps):
        '''
        Test the retrieved interface status against the expected result.
        '''
        for interface in self.interfaces:
            with steps.start(
                f"Validating {interface['portName']}",
                continue_=True
            ) as step:
                try:
                    assert interface["status"] == "up"
                except:
                    step.failed(f"{interface['portName']} is ❌ DOWN ❌")
                else:
                    step.passed(f"{interface['portName']} is ✅ UP ✅")

    @aetest.cleanup
    def cleanup(self):
        ''' No cleanup needed for this Catalyst Center testcase '''
        pass

if __name__ == "__main__":
    import os
    cat_creds = {
        "url": "sandboxdnac.cisco.com",
        "username": "devnetuser",
        "password": "Cisco123!"
    }
    devices = (
        {"name":"my_switch", "uuid":"04591e4f-de5e-4683-8b89-cb5dc5699df2"},
    )

    aetest.main(device_list=devices, cat_creds=cat_creds)
