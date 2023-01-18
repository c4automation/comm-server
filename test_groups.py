import pytest


@pytest.mark.parametrize("name,extension,call_type", [
    ('group 1', 101, 'Hunt'),
    ('group2', 102, 'Ring-All'),
    ('All', 10, 'Hunt'),
    ('Everyone', 0, 'Ring-All'),
    ('MY $)* group', 100, 'Ring-All'),
    ])
def test_add_group(setup, name, extension, call_type):
    server = setup

    response = server.add_group(name=name, extension=extension, call_type=call_type)
    assert response.status_code == 200

@pytest.mark.parametrize("name,extension,call_type", [
    ('group2', 103, 'Hunt'),    # Name in use
    ('group 4', 102, 'Hunt'),    # Ext in use
    ('group 5', 105, 'foo'),    # Invalid call_type
    ('group 6', 106, 'HUNT'),    # Invalid type: Should be 'Hunt'
    ('Big long group name@$% with !@#$', 106, 'RING-ALL'),    # Invalid call_type
    (None, 107, 'Hunt'),
    ('my group 8', None, 'Hunt'),
    ('my group 9', 109, None),
    ('my group 9', "s", "Ring-All"),
])
def test_add_group_invalid(setup, name, extension, call_type):
    server = setup
    response = server.add_group(name=name, extension=extension, call_type=call_type)
    assert response.status_code == 400   # FIXME


@pytest.mark.xfail()
def test_get_group(setup):
    server = setup
    response = server.get_group('group 1')

    assert response.status_code == 200
    group = response.json()

    assert group['name'] == 'group 1'
    assert group['extension'] == 101
    assert group['call_type'] == 'Hunt'

def test_get_groups(setup):
    server = setup
    response = server.get_group()

    assert response.status_code == 200
    groups = response.json()
    assert len(groups) == 5

def test_get_group_badname(setup):
    server = setup
    response = server.get_group('not_a_group')
    assert response.status_code >= 404 # FIXME


@pytest.mark.parametrize('name,extension,call_type', [
    ('group 1', 912, 'Hunt'),
    ('group2', 911, 'Hunt'),
])
def test_update_group_valid(setup, name, extension, call_type):
    server = setup
    response = server.update_group(name=name, extension=extension, call_type=call_type)
    assert response.status_code == 200

    group = response.json()
    assert group['extension'] == extension
    assert group['call_type'] == call_type

@pytest.mark.parametrize('name,extension,call_type', [
    ('group 1', 911, 'Hunt'),  # ext in use
    ('group2', 911, 'FOO'),   # invalid call_type
    ('group foo', 999, 'Hunt'),   # invalid group
])
def test_update_group_invalid(setup, name, extension, call_type):
    server = setup
    ret = server.update_group(name=name, extension=extension, call_type=call_type)

    assert 400 <= ret.status_code < 500   # FIXME returns 500 right now

def test_delete_group(setup):
    server = setup
    ret = server.delete_group('group2')
    assert ret.status_code == 200

    ret = server.delete_group('group2')
    assert ret.status_code >= 404   # FIXME

def test_delete_group2(setup):
    server = setup
    ret = server.delete_group('not_here')
    assert ret.status_code >= 404  # FIXME returns 500
