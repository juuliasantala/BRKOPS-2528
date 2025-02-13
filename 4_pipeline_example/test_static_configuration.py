#!/usr/bin/env python
'''
A simple test to execute a static configuration analysis.

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

import ipaddress
import sys
from pyats import aetest
import yaml

class CommonSetup(aetest.CommonSetup):

    @aetest.subsection
    def read_configuration(self, config_file):

        with open(config_file, encoding="utf-8") as my_values:
            config = yaml.safe_load(my_values.read())

        aetest.loop.mark(InterfaceConfigAnalysis, site=config)

class InterfaceConfigAnalysis(aetest.Testcase):

    @aetest.setup
    def loop_interfaces(self, site):
        aetest.loop.mark(self.validate_address, device=site["devices"])

    @aetest.test
    def validate_address(self, steps, device):

        for interface in device["interfaces"]:
            with  steps.start(f"Validating IP address for {interface['type']} {interface['number']}", continue_=True) as step:
                
                address = interface["address"]

                try:
                    ipaddress.IPv4Address(address)
                except Exception as err:
                    step.failed(f"{address} is not a valid ip address: {err}")
                else:
                    step.passed(f"{address} is a valid ip address")

if __name__ == "__main__":

    config_test = aetest.main(config_file="interface_config.yaml")

    if str(config_test) != "passed":
        sys.exit(1)