import pytest


def test_get_network_status(setup):
    server = setup
    response = server.get_network_status()
    print(response.text)
    assert response.status_code == 200


def test_get_user_list(setup):
    server = setup
    response = server.get_user_list()
    print(response.text)
    assert response.status_code == 200
