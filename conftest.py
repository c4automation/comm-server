
import pytest
from intercom_common.commserver import CommServer
from comm_utils import reset_database


def pytest_addoption(parser):
    """Add the --address command line arg to pytest"""
    parser.addoption('--address', action='store', help='IP address of comm server', required=True)
    parser.addoption('--keep_db', action='store_true', help="Don't delete the Comm server database", default=False)


#
@pytest.fixture(scope='session')
def setup(request):
    ip = request.config.getoption('--address')
    keep_db = request.config.getoption('--keep_db')
    if not keep_db:
        reset_database(ip)
    return CommServer("http://{}".format(ip))

