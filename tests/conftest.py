import icecream
import pytest
from src.core.transfero.synonyms import setup_wn


@pytest.fixture(scope="session", autouse=True)
def install_icecream():
    icecream.install()


@pytest.fixture(scope="session", autouse=True)
def initialise_wn():
    setup_wn()


def pytest_configure(config):
    if config.getoption("--snapshot-update"):
        config.pluginmanager.set_blocked("dsession")
