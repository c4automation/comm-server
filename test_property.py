import pytest
from intercom_common.commserver import CommServer


@pytest.mark.parametrize("user_id,password,accountCode,user_context,effective_caller_id_name,effective_caller_id_number,success", [
    ('300', 'test1234', '300', 'default', 'test', '200', True),
    ('300', 'test1234', '300', 'default', 'mytest', '200', False),# name in use
    ('400', 'test5678', '400', 'default', 'mytest', '201', True), # should add fine

#    pytest.param('res3', '10.0.0.1', 3, False,   # ip in use
#                 marks=pytest.mark.xfail),
    ('500', 'fun1234', '400', 'default', 'testpart2', '500', True),   #
    ('300', 'fun1234', '400', 'default', 'testpart2', '500', False),  # Verify that after second room is added cannot add another '300' extension
#    ('res4', '10.0.0.4', 4, True),
#    ('res 5', '192.168.1.240', 9004, True),
#    ('res foo ()#*$(31', '10.0.0.10', 2322, True),   # crazy chars in name

 #   pytest.param('res6', '10.0.0.01', 6, False, marks=pytest.mark.xfail),   # ip in use
    ])
def test_add_property_device(setup, user_id, password, accountCode, user_context, effective_caller_id_name, effective_caller_id_number, success):
    x = setup
    c = x.add_property_device(user_id, password, accountCode, user_context, effective_caller_id_name, effective_caller_id_number)
    if success:
        assert c == 200
    else:
        assert c != 200

def test_get_property_device(setup):
    server = setup
    res = server.get_property_device()
    print ("The answer is {} ".format(res))
#    assert len(res) == 6

def test_check_first_device(setup):
    fValue = True
    server = setup
    getRequest = server.get_property_device()

    if (getRequest[0]['domain'] != '192.168.1.102') or (getRequest[0]['password'] != 'test1234') or (getRequest[0]['user_id'] != 300)\
                or (getRequest[0]['effective_caller_id_name'] != 'test') or (getRequest[0]['effective_caller_id_number'] != 200):
        fValue = False

#    if (getRequest[0]['domain'] != '192.168.1.102')\
#           or (getRequest[0]['password'] != 'test1234'):
#        fValue = False

    assert fValue == True
#    print ("{}".format(fValue))

#    for index in range(len(getRequest)):
#        for key in getRequest[index]:
#            print ("{}".format(getRequest[index][key]))

def test_update_property_device(setup):
    server = setup
    # TODO: PUT request fails in DB, var oldExtension is undefined.
    res = server.update_property_device('300', '300', 'test55', '300', 'default', 'test', '600')
    assert res == 200

def test_update_second_device(setup):
    server = setup
    # TODO: PUT request fails in DB, var oldExtension is undefined.
    res = server.update_property_device('500', '500', 'fun55', '500', 'default', 'test2', '700')
    getRequest = server.get_property_device()
    print("{}".format(getRequest))
    assert res == 200

def test_check_updates(setup):
    fValue = True
    server = setup

    getRequest = server.get_property_device()

    if (getRequest[0]['domain'] != '192.168.1.102') or (getRequest[0]['password'] != 'test55') or (getRequest[0]['user_id'] != 300)\
                or (getRequest[0]['effective_caller_id_name'] != 'test') or (getRequest[0]['effective_caller_id_number'] != 600):
        fValue = False

    if (getRequest[2]['domain'] != '192.168.1.102') or (getRequest[2]['password'] != 'fun55') or (getRequest[2]['user_id'] != 500)\
                or (getRequest[2]['effective_caller_id_name'] != 'test2') or (getRequest[2]['effective_caller_id_number'] != 700):
        fValue = False

    assert fValue

@pytest.mark.parametrize("unit_id,success", [
    pytest.param('300', True),
    ('400', True),
    ])
def test_delete_property_device(setup, unit_id, success):
    server = setup
    c = server.delete_property_device(unit_id)

    if success:
        assert c == 200
    else:
        assert c != 200


