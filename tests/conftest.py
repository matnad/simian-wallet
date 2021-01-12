#!/usr/bin/python3
import pytest


@pytest.fixture(scope="function", autouse=True)
def isolate(fn_isolation):
    pass


@pytest.fixture(scope="module")
def zero_addr():
    yield "0x0000000000000000000000000000000000000000"


@pytest.fixture(scope="module")
def all_addr():
    yield "0xffffffffffffffffffffffffffffffffffffffff"


@pytest.fixture(scope="module")
def deployer(accounts):
    yield accounts[0]


@pytest.fixture(scope="module")
def owner(accounts):
    yield accounts[1]


@pytest.fixture(scope="module")
def user(accounts):
    yield accounts[5]


@pytest.fixture(scope="module")
def user2(accounts):
    yield accounts[6]


@pytest.fixture(scope="module")
def lgt(interface):
    yield interface.ILGT("0x000000000000C1CB11D5c062901F32D06248CE48")


@pytest.fixture(scope="module")
def chi(interface):
    yield interface.ICHI("0x0000000000004946c0e9f43f4dee607b0ef1fa1c")



@pytest.fixture(scope="module")
def router2(interface):
    yield interface.IUniswapV2Router02("0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D")


@pytest.fixture(scope="module")
def weth(interface):
    yield interface.IERC20("0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2")


@pytest.fixture(scope="module")
def usdt(interface):
    yield interface.IERC20("0xdAC17F958D2ee523a2206206994597C13D831ec7")


@pytest.fixture(scope="module")
def dai(interface):
    yield interface.IERC20("0x6B175474E89094C44Da98b954EedeAC495271d0F")


@pytest.fixture(scope="module")
def sushi(interface):
    yield interface.IERC20("0x6B3595068778DD592e39A122f4f5a5cF09C90fE2")


@pytest.fixture(scope="module")
def aave(interface):
    yield interface.IERC20("0x7Fc66500c84A76Ad7e9c93437bFc5Ac33E2DDaE9")


@pytest.fixture(scope="module")
def cream(interface):
    yield interface.IERC20("0x2ba592F78dB6436527729929AAf6c908497cB200")


@pytest.fixture(scope="module")
def crv(interface):
    yield interface.IERC20("0xD533a949740bb3306d119CC777fa900bA034cd52")


@pytest.fixture(scope="module")
def usdc(interface):
    yield interface.IERC20("0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48")


@pytest.fixture(scope="module")
def susd(interface):
    yield interface.IERC20("0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48")


@pytest.fixture(scope="module")
def mic(interface):
    yield interface.IERC20("0x368B3a58B5f49392e5C9E4C998cb0bB966752E51")


@pytest.fixture(scope="module")
def wbtc(interface):
    yield interface.IERC20("0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599")


@pytest.fixture(scope="module")
def do_expensive(DoExpensive, deployer):
    yield DoExpensive.deploy({'from': deployer})


@pytest.fixture(scope="module")
def do_nothing(DoNothing, deployer):
    yield DoNothing.deploy({'from': deployer})


@pytest.fixture(scope="module")
def do_malicious(DoMalicious, deployer):
    yield DoMalicious.deploy({'from': deployer})


@pytest.fixture(scope="module")
def do_test(DoTest, deployer):
    yield DoTest.deploy({'from': deployer})


@pytest.fixture(scope="function")
def lgt_strategy(LgtStrategy, deployer):
    yield LgtStrategy.deploy({'from': deployer})


@pytest.fixture(scope="function")
def wallet(SimianWallet, deployer, owner):
    wallet = SimianWallet.deploy({'from': deployer})
    deployer.transfer(wallet, "10 ether")
    wallet.transferOwnership(owner)
    yield wallet


