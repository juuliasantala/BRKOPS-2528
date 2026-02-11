#!/usr/bin/env python
'''
pyATS test to validate ping connectivity.

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

from pyats import aetest, topology

class CommonSetup(aetest.CommonSetup):

    @aetest.subsection
    def connect_to_devices(self, testbed):
        testbed.connect(log_stdout=False, learn_hostname=True)

    @aetest.subsection
    def mark_tests_for_looping(self, testbed):
        aetest.loop.mark(PingTestcase, device=testbed.devices.values())

class PingTestcase(aetest.Testcase):

    @aetest.test
    def ping(self, steps, device, destinations):
        for destination in destinations:
            with steps.start(
                f"{device.hostname} -> {destination} ", continue_=True
                ) as step:
                try:
                    device.ping(destination)
                except:
                    step.failed(f'Ping {destination} from device {device} unsuccessful')
                else:
                    step.passed(f'Ping {destination} from device {device} successful')

class CommonCleanup(aetest.CommonCleanup):

    @aetest.subsection
    def disconnect_from_devices(self, testbed):
        testbed.disconnect()

if __name__ == "__main__":

    my_destinations = (
        '8.8.8.8',
        '198.18.10.10',
        '198.18.20.10'
        )

    my_testbed = topology.loader.load("testbed.yaml")
    ping_test = aetest.main(testbed=my_testbed, destinations=my_destinations)
