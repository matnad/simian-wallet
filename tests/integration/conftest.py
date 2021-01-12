#!/usr/bin/python3
import pytest


@pytest.fixture(scope="module")
def sushiswap(interface):
    yield interface.IUniswapV2Router02('0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F')


@pytest.fixture(scope="module")
def to_erc20(interface):
    yield lambda addr: interface.IERC20(addr)


@pytest.fixture(scope="module")
def deploy_farm(deployer, StakingRewards):
    def deploy_f(reward_token, staking_token, initial_funding):
        initial_funding = initial_funding * 10 ** reward_token.decimals()
        if reward_token.balanceOf(deployer) < initial_funding:
            raise ValueError(f"Deployer has insufficient {reward_token.symbol()}.")
        farm = StakingRewards.deploy(
            deployer, deployer, reward_token, staking_token, 86400, {'from': deployer}
        )
        reward_token.approve(farm, 2**256 - 1, {'from': deployer})
        farm.notifyRewardAmount(initial_funding, {'from': deployer})
        return farm
    yield deploy_f


@pytest.fixture(scope="function")
def snx_proxy(deployer, HarvestFarms):
    yield HarvestFarms.deploy({'from': deployer})
