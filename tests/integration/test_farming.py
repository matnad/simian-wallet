import pytest
from brownie import *

"""
Still a work in progress.
"""

def sushiswap_swap(sushiswap, user, token_in, token_out):
    """ Swap all `token_in` to `token_out` via WETH pair. Unspecified `token_out` means ETH. """
    path = [token_in, "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2", token_out]
    deadline = chain[-1].timestamp + 3600
    func = sushiswap.swapExactTokensForTokens
    params = {'from': user}
    if token_in.allowance(user, sushiswap) == 0:
        token_in.approve(sushiswap, 2 ** 256 - 1, params)

    balance = token_out.balanceOf(user)
    func(token_in.balanceOf(user), 0, path, user, deadline, params)
    profit = token_out.balanceOf(user) - balance
    print(f"Swapped it!  +${profit/1e6:.2f} USDT")


def sushiswap_buy_token(
        sushiswap, user, receiver, token, token_amount, max_eth_amount, additional_paths=None
):
    """ Buy token with ETH """
    path = ["0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2", token]
    if additional_paths:
        path = ["0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2", *additional_paths, token]
    sushiswap.swapETHForExactTokens(
        token_amount,
        path,
        receiver,
        chain.time() + 1000,
        {"from": user, "value": max_eth_amount}
    )


@pytest.mark.parametrize("strategy", ("none", "lgt"))
def test_harvest_farms(
        wallet, sushiswap,
        owner, user, deployer,
        aave, usdt, susd, cream, crv, usdc, mic,
        deploy_farm, snx_proxy, lgt_strategy, strategy
):
    gas_price = "250 gwei"
    # Deploy Farms
    staking_tokens = [aave, susd, cream, crv, usdc]
    staking_amounts = [1000, 120000, 2000, 150000, 100000]
    staking_amounts = [a * 10 ** t.decimals() for a, t in zip(staking_amounts, staking_tokens)]
    reward_amount = 50000
    farms = []
    reward_token = mic
    total_rewards = reward_amount * len(staking_tokens) * 10 ** reward_token.decimals()
    sushiswap_buy_token(sushiswap, deployer, deployer, reward_token, total_rewards, "500 ether", additional_paths=[usdt])
    for staking_token, stake_amount in zip(staking_tokens, staking_amounts):
        farm = deploy_farm(reward_token, staking_token, reward_amount)
        farms.append(farm)
        sushiswap_buy_token(sushiswap, user, wallet, staking_token, stake_amount, "300 ether")

    if strategy == "lgt":
        wallet.setDefaultStrategy(lgt_strategy, {'from': owner})
    balance = owner.balance()

    # stake in farms
    data = snx_proxy.stake.encode_input(staking_amounts, farms, staking_tokens)
    wallet.execute(snx_proxy, data, {'from': owner, 'gas_price': gas_price})

    # get rewards as usdt
    chain.sleep(int(60 * 60 * 5))  # wait 5 hours
    data = snx_proxy.getRewardsAs.encode_input(farms, reward_token, usdt)
    wallet.execute(snx_proxy, data, {'from': owner, 'gas_price': gas_price})
    print("Rewards received:", usdt.balanceOf(wallet) * 10 ** -6, "USDT.")

    # get rewards
    chain.sleep(int(60 * 60 * 5))  # wait 5 hours
    data = snx_proxy.getRewards.encode_input(farms)
    wallet.execute(snx_proxy, data, {'from': owner, 'gas_price': gas_price})
    print(
        "Rewards received:",
        reward_token.balanceOf(wallet) * 10 ** -reward_token.decimals(),
        reward_token.symbol()
    )

    # Total Gas Cost
    print(f"Gas Spent with strategy {strategy}: {(balance - owner.balance()).to('ether')}.")



