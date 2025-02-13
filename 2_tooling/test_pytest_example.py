import ipaddress

def test_network():
    address = ipaddress.ip_address("10.10.10.10")
    network = ipaddress.ip_network("10.10.10.0/24")

    assert address in network
