import time
import pytest


def test_get_system_clock(setup):
    server = setup
    response = server.get_system_clock()
    assert response.status_code == 200

    clock = response.json()

    assert 'time' in clock
    assert 'setBy' in clock
    assert 'timezone' in clock
    assert 'ntp' in clock


def test_get_system_network(setup):
    server = setup
    response = server.get_system_network()
    assert response.status_code == 200

    network = response.json()
    assert 'dns' in network
    assert 'domain' in network

def test_get_info(setup):
    server = setup
    response = server.get_info()
    assert response.status_code == 200


def test_update_url(setup):
    server = setup
    response = server.update_url()
    print(response.text)
    assert response.status_code == 200

    data = response.json()
    assert data['url'] == "http://update2.control4.com/communication/release/latest.json"


def test_ping_server(setup):
    server = setup
    response = server.ping_server()
    assert response.status_code == 200


@pytest.mark.slow
def test_reboot_server(setup):
    server = setup
    response = server.reboot_server()
    #assert response.status_code == 200
    time.sleep(30)
    response = server.ping_server()
    assert response.status_code == 200


@pytest.mark.slow
def test_restore_server(setup):
    server = setup
    response = server.restore_server()
    assert response.status_code == 200
    print(response)
    time.sleep(30)

    # Check that data is all deleted
    data = server.get_residence()
    #assert response.status_code == 200
    print(data)

    assert len(data) == 0
