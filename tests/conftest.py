import icecream
import pytest


@pytest.fixture(scope="session", autouse=True)
def install_icecream():
    icecream.install()


def pytest_configure(config):
    if config.getoption("--snapshot-update"):
        config.pluginmanager.set_blocked("dsession")
