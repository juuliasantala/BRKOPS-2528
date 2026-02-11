#!/usr/bin/env python
'''
Simple test to validate OSPF neighbor state.

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

from netmiko import ConnectHandler

DEVICE = {
    "device_type": "cisco_ios",
    "host": "198.18.200.14",
    "username": "netadmin",
    "password": "C1sco12345",
    "port": 22
}

def test_ospf_neighbors():

    conn = ConnectHandler(**DEVICE)
    output = conn.send_command("show ip ospf neighbor")
    conn.disconnect()
    
    print(f"\nOSPF Neighbors:\n{output}")
    
    assert output.strip(), "No output received from device"
    assert "FULL" in output, "No OSPF neighbors in FULL state found"
