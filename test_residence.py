import pytest


@pytest.mark.parametrize("name,ipaddr,ext,success", [
    ('res1', '10.0.0.1', 1, True),
    ('res1', '10.0.0.2', 2, False),   # name in use

    ('res3', '10.0.0.1', 3, False),   # ip in use
    ('res4', '10.0.0.4', 3, False),   # ext in use
    ('res4', '10.0.0.4', 4, True),
    ('res 5', '192.168.1.240', 9004, True),
    ('res foo ()#*$(31', '10.0.0.10', 2322, True),   # crazy chars in name

    pytest.param('res6', '10.0.0.01', 6, False, marks=pytest.mark.xfail),   # ip in use
    ])
def test_add_residence(setup, name, ipaddr, ext, success):
    x = setup
    c = x.add_residence(name=name, ipaddress=ipaddr, extension=ext)
    if success:
        assert c == 200
    else:
        assert c != 200


def test_get_residence(setup):
    server = setup
    res = server.get_residence()
    assert len(res) == 6


def test_get_residence_byname(setup):
    server = setup
    res = server.get_residence('res4')
    assert len(res) == 1

    res = res[0]
    assert res['name'] == 'res4'
    assert res['realm'] == '10.0.0.4'
    assert res['extension'] == 4
    assert res['intercom_group'] == 'All'


def test_get_residence_by_bad_name(setup):
    server = setup
    res = server.get_residence('foo1')
    assert res is None


@pytest.mark.xfail
def test_update_residence(setup):
    server = setup
    # TODO: PUT request fails in DB, var oldExtension is undefined.
    res = server.update_residence('res4', '172.0.0.1')
    assert res == 200


@pytest.mark.parametrize("name,success", [
    pytest.param('res1', True, marks=pytest.mark.xfail),
    ('res1', False),
    ('foobar', False),
    ('res 5', True),
    ])
def test_delete_residence(setup, name, success):
    server = setup
    c = server.delete_residence(name)

    if success:
        assert c == 200
    else:
        assert c != 200


#@pytest.mark.xfail
def test_delete_all_residences(setup):
    server = setup
    ok = server.delete_all_residences()
    assert ok

    res = server.get_residence('res1')
    assert res is None

    res = server.get_residence()
    assert len(res) == 0
