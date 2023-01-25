import random

import os

from tempfile import mkstemp

import pytest

from BdrcDbLib.DbOrm.DrsContextBase import DrsDbContextBase

config_file_tag: str = ""


@pytest.fixture(autouse=True)
def test_wrapper():
    """
    Create the config file used in the tests
    """
    conf_file = mkstemp(prefix=".DrsDbContextTest", suffix=".config", text=True)
    global config_file_tag
    env_key: str = "_GEN_CONFIG"
    with open(conf_file[0], "w", newline='\n') as cf:
        cf.writelines(["[mysql]\n", f"mySqlCnfPath = {os.getenv(env_key)}\n", "[test]\n", "server = RDSAWSQAClient\n"])

    config_file_tag = f"test:{conf_file[1]}"
    # Override default for test
    DrsDbContextBase.bdrc_db_conf = config_file_tag
    yield
    os.remove(conf_file[1])


def test_session():
    with DrsDbContextBase() as conn:
        assert conn.session


def test_get_session():
    with DrsDbContextBase() as conn:
        assert conn.get_session()


def test_connect_db():
    with DrsDbContextBase() as conn:
        assert conn.connect_db(config_file_tag)


def test_get_some_works():
    with DrsDbContextBase() as conn:
        # e: Engine  = conn.connect_db(config_file_tag)
        blarg = conn.get_some_works()
        assert blarg


def test_get_work_by_name():
    with DrsDbContextBase() as conn:
        # e: Engine  = conn.connect_db(config_file_tag)
        expected_work_name = 'W1FPL2251'
        fetched_work = conn.get_work_by_name(expected_work_name)
        assert expected_work_name == fetched_work.WorkName


def test_get_or_create_work():
    with DrsDbContextBase() as conn:
        # e: Engine  = conn.connect_db(config_file_tag)
        expected_work_name = 'W1FPL2251'
        fetched_work = conn.get_or_create_work(expected_work_name)
        assert expected_work_name == fetched_work.WorkName

        rname = f"{int(random.uniform(599, 29899))}"
        new_work = conn.get_or_create_work(f"WXTest-{rname}")

        # Assumes integer incrementing key
        assert new_work.workId > fetched_work.workId

        # cleanup on aisle 5
        conn.session.delete(new_work)
        conn.session.commit()


@pytest.mark.skip(reason="We're just testing connectivity")
def test_get_or_create_volume():
    pass

@pytest.mark.skip(reason="We're just testing connectivity")
def test_get_downloads():
    pass
