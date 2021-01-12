#!/usr/bin/python3
import pytest


@pytest.fixture(scope="module")
def strategy_sig():
    yield "0xc893a971"


@pytest.fixture(scope="module")
def empty_strategy(EmptyStrategy, deployer):
    yield EmptyStrategy.deploy({'from': deployer})


@pytest.fixture(scope="module")
def empty_strategy2(EmptyStrategy2, deployer):
    yield EmptyStrategy2.deploy({'from': deployer})
